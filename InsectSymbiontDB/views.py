from django.http import HttpResponse
from django.shortcuts import render
from subprocess import Popen, PIPE
import os
from django.conf import settings
import uuid
from django.http import JsonResponse
from .scripts.batch_search_tool import (
    read_symbiont_db, match_species_level, match_genus_level,
    filter_genus_matches, add_order_matching, add_insect_matching,
    filter_matches, write_results
)
from metagenome.models import Metagenome
from amplicon.models import Amplicon
from django.db.models import Q
import logging
from django.views.decorators.csrf import csrf_exempt
from .scripts import kraken_convert, krona_convert
import json
from django.core.files.storage import default_storage
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger(__name__)


def test(request):
    return render(request, "test.html")

def home(request):
    return render(request, "home.html")

def network(request):
    return render(request, "network.html")

def resources(request):
    return render(request, "resources.html")

def blast(request):
    return render(request, "tools/blast.html")

def blast_search(request):
    if request.method == 'POST':
        sequence = request.POST.get('q', '')
        blast_type = request.POST.get('blast')
        database = request.POST.get('db')
        e_value = request.POST.get('e')

        # 保存输入序列到临时文件
        tmp_dir = os.path.join(BASE_DIR, 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)  # 如果目录不存在则创建
        query_file = os.path.join(tmp_dir, "tmp_query.fasta")

        # 检查文件上传或文本框输入
        if sequence:
            with open(query_file, "w") as f:
                f.write(sequence)
        elif 'input' in request.FILES:
            uploaded_file = request.FILES['input']
            with open(query_file, "wb") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
        else:
            # 如果既没有输入序列也没有上传文件，则返回错误提示
            return HttpResponse("Please enter a sequence or upload a file.")

        # 数据库路径
        db_dir = os.path.join(BASE_DIR, 'media/blast_db')
        db_path = os.path.join(db_dir, database)

        # 构建 BLAST 命令
        blast_cmd = f"{blast_type} -query {query_file} -db {db_path} -evalue {e_value} -outfmt 6"
        process = Popen(blast_cmd, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        # 删除临时文件
        os.remove(query_file)

        # 处理 BLAST 输出，将其按列分割
        blast_results = []
        for line in stdout.decode('utf-8').strip().split('\n'):
            columns = line.split('\t')
            blast_results.append({
                'query_id': columns[0],
                'subject_id': columns[1],
                'identity': columns[2],
                'alignment_length': columns[3],
                'mismatches': columns[4],
                'gap_opens': columns[5],
                'q_start': columns[6],
                'q_end': columns[7],
                's_start': columns[8],
                's_end': columns[9],
                'e_value': columns[10],
                'bit_score': columns[11],
            })

        # 渲染结果页面
        return render(request, 'tools/blast_result.html', {'results': blast_results})

    return render(request, 'tools/blast.html')

def batch_search(request):
    """处理批量搜索请求"""
    if request.method == 'POST':
        print("Received POST request")

        try:
            # 获取表单数据
            host_order = request.POST.get('host_order')
            host_name = request.POST.get('host_name')
            file_type = request.POST.get('file_type', 'kraken')  # 默认为 kraken 格式

            print(f"Host Order: {host_order}")
            print(f"Host Name: {host_name}")
            print(f"File Type: {file_type}")

            # 验证必要参数
            if not host_order or not host_name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Host order and name are required'
                })

            # 生成唯一的文件标识符
            file_id = str(uuid.uuid4())
            print(f"Generated file ID: {file_id}") # 调试日志

            # 创建临时文件来存储输入数据
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'batch_search', 'temp')
            os.makedirs(temp_dir, exist_ok=True)

            input_file_path = os.path.join(temp_dir, f"{file_id}_input.txt")

            # 处理输入数据
            if 'file' in request.FILES:
                print("Processing uploaded file") # 调试日志
                input_file = request.FILES['file']
                with open(input_file_path, 'wb+') as destination:
                    for chunk in input_file.chunks():
                        destination.write(chunk)
            elif 'text_input' in request.POST:
                print("Processing text input") # 调试日志
                text_input = request.POST.get('text_input')
                if not text_input:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'No input data provided'
                    })
                with open(input_file_path, 'w', encoding='utf-8') as f:
                    f.write(text_input)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No input data provided'
                })

            # 设置输出文件路径
            results_dir = os.path.join(settings.MEDIA_ROOT, 'batch_search', 'results')
            os.makedirs(results_dir, exist_ok=True)

            all_results_file = os.path.join(results_dir, f"{file_id}_all_matches.txt")
            filtered_results_file = os.path.join(results_dir, f"{file_id}_filtered_matches.txt")

            print(f"Output files: \nAll: {all_results_file}\nFiltered: {filtered_results_file}") # 调试日志

            try:
                # 读取共生菌数据库
                symbiont_db = read_symbiont_db(os.path.join(settings.BASE_DIR, "symbiontsDB.txt"))
                print(f"Loaded symbiont database with {len(symbiont_db)} entries") # 调试日志

                # 进行物种级别的比对，传入文件类型
                species_matches = match_species_level(input_file_path, symbiont_db, file_type)
                print(f"Found {len(species_matches)} species matches") # 调试日志

                # 进行属级别的比对，传入文件类型
                genus_matches = match_genus_level(input_file_path, symbiont_db, file_type)
                print(f"Found {len(genus_matches)} genus matches") # 调试日志

                # 过滤属级别的匹配结果
                filtered_genus_matches = filter_genus_matches(species_matches, genus_matches)

                # 合并所有匹配结果
                all_matches = species_matches + filtered_genus_matches

                # 如果没有找到任何匹配结果
                if not all_matches:
                    return JsonResponse({
                        'status': 'no_matches',
                        'message': 'No matching symbiont records found. Please check if your input format is correct and try again.'
                    })

                # 添加目匹配信息
                all_matches = add_order_matching(all_matches, host_order)

                # 添加昆虫物种匹配信息
                all_matches = add_insect_matching(all_matches, host_name)

                # 按评分排序
                sorted_matches = sorted(all_matches, key=lambda x: x['total_score'], reverse=True)

                # 保存所有匹配结果
                write_results(sorted_matches, all_results_file)

                # 最终筛选（每个共生菌最多保留3条记录）
                final_matches = filter_matches(sorted_matches, max_records=3)

                # 保存筛选后的结果
                write_results(final_matches, filtered_results_file)

                print("Processing completed successfully") # 调试日志

                # 返回结果
                return JsonResponse({
                    'status': 'success',
                    'data': {
                        'all_results_file': f"/media/batch_search/results/{os.path.basename(all_results_file)}",
                        'filtered_results_file': f"/media/batch_search/results/{os.path.basename(filtered_results_file)}",
                        'filtered_results': final_matches[:50]  # 返回前10条结果用于预览
                    }
                })

            except Exception as e:
                print(f"Error during processing: {str(e)}") # 调试日志
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error processing data: {str(e)}'
                })

            finally:
                # 清理临时文件
                if os.path.exists(input_file_path):
                    os.remove(input_file_path)

        except Exception as e:
            print(f"Error in request handling: {str(e)}") # 调试日志
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    # GET 请求返回页面
    return render(request, 'tools/batch_search.html')

def map(request):
    return render(request, "tools/map.html")

def compare(request):
    return render(request, "tools/composition_compare.html")

# def literatures(request):

#     return render(request, "literatures.html")

def hosts(request):
    return render(request, "hosts.html")

def contact(request):
    return render(request, "contact.html")

def help(request):
    return render(request, "help.html")

def get_samples(request):
    """API endpoint to get samples for composition comparison"""
    sample_type = request.GET.get('type', '')
    species_filter = request.GET.get('species', '')

    samples = []

    try:
        if sample_type == 'metagenome':
            # 构建查询
            query = Metagenome.objects.all()

            # 应用物种过滤器
            if species_filter:
                query = query.filter(host__icontains=species_filter)

            # 限制返回数量，避免过多数据
            query = query[:100]

            # 格式化结果
            samples = [
                {
                    'id': meta.id,
                    'run': meta.run,
                    'host': meta.host or 'Unknown',
                    'country': meta.geo_loc_name_country or 'NA',
                    'assay_type': meta.assay_type or 'Metagenome'
                }
                for meta in query
            ]

        elif sample_type == 'amplicon':
            # 构建Amplicon查询
            query = Amplicon.objects.all()

            # 应用物种过滤器
            if species_filter:
                query = query.filter(host__icontains=species_filter)

            # 限制返回数量，避免过多数据
            query = query[:100]

            # 格式化结果，确保处理空值
            samples = [
                {
                    'id': amp.id,
                    'run': amp.run or 'Unknown',
                    'host': amp.host or 'Unknown host',
                    'country': amp.geo_loc_name_country or 'NA',
                    'assay_type': amp.assay_type or 'Amplicon'
                }
                for amp in query
            ]

        return JsonResponse({
            'samples': samples
        })

    except Exception as e:
        # 记录错误并返回友好的错误消息
        print(f"Error in get_samples: {str(e)}")
        return JsonResponse({
            'error': 'An error occurred while fetching samples',
            'message': str(e),
            'samples': []
        }, status=500)

def get_taxonomic_composition(request):
    """获取样本的物种组成数据"""
    try:
        logger.info(f"Received request with params: {request.GET}")
        sample_runs = request.GET.getlist('samples[]')
        sample_types = request.GET.getlist('types[]')
        taxonomic_level = request.GET.get('level', 'Genus')

        logger.info(f"Processing request for {len(sample_runs)} samples at {taxonomic_level} level")

        # 将分类级别首字母大写，以匹配文件中的格式
        taxonomic_level = taxonomic_level.capitalize()

        if not sample_runs or not sample_types or len(sample_runs) != len(sample_types):
            return JsonResponse({
                'error': 'Invalid parameters'
            }, status=400)

        # 存储所有样本的数据
        all_sample_data = []
        missing_samples = []

        # 处理每个样本
        for run_id, sample_type in zip(sample_runs, sample_types):
            # 确保类型是正确的
            sample_type = sample_type.lower()  # 转换为小写以确保匹配
            if sample_type not in ['metagenome', 'amplicon', 'custom']:
                logger.warning(f"Invalid sample type: {sample_type} for sample {run_id}")
                missing_samples.append(run_id)
                continue

            # 构建文件路径
            if sample_type == 'custom':
                file_path = os.path.join(settings.MEDIA_ROOT, 'custom', run_id, f'{run_id}.compare.txt')
            else:
                file_path = os.path.join(settings.MEDIA_ROOT, sample_type, run_id, f'{run_id}.compare.txt')

            logger.info(f"Checking file path: {file_path}")

            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                missing_samples.append(run_id)
                continue

            # 读取并解析文件
            taxa_data = {}
            try:
                with open(file_path, 'r') as f:
                    logger.debug(f"Reading file for sample {run_id}")
                    for line in f:
                        try:
                            abundance, level, taxon = line.strip().split('\t')
                            # 添加调试日志
                            logger.debug(f"Line data - Level: {level}, Requested: {taxonomic_level}")
                            if level == taxonomic_level:
                                taxa_data[taxon] = float(abundance)
                        except ValueError as e:
                            logger.warning(f"Invalid line format in {run_id}: {line.strip()}")
                            continue

                if taxa_data:
                    logger.info(f"Found {len(taxa_data)} taxa for {run_id} at {taxonomic_level} level")
                    all_sample_data.append({
                        'sample_id': run_id,
                        'taxa': taxa_data
                    })
                else:
                    logger.warning(f"No data found for taxonomic level {taxonomic_level} in sample {run_id}")
                    missing_samples.append(run_id)

            except Exception as e:
                logger.error(f"Error processing file for sample {run_id}: {str(e)}")
                missing_samples.append(run_id)
                continue

        # 检查是否有有效数据
        if not all_sample_data:
            return JsonResponse({
                'error': 'No valid data found for any selected samples',
                'missing_samples': missing_samples
            }, status=404)

        # 获取所有样本中出现的taxa
        all_taxa = set()
        for sample in all_sample_data:
            all_taxa.update(sample['taxa'].keys())

        # 格式化返回数据
        formatted_data = {
            'samples': [sample['sample_id'] for sample in all_sample_data],
            'taxa': list(all_taxa),
            'abundances': [],
            'missing_samples': missing_samples
        }

        # 为每个taxon准备数据
        for taxon in formatted_data['taxa']:
            abundances = []
            for sample in all_sample_data:
                abundances.append(sample['taxa'].get(taxon, 0))
            formatted_data['abundances'].append(abundances)

        # 在返回数据之前添加日志
        logger.info(f"Returning data with {len(formatted_data['samples'])} samples and {len(formatted_data['taxa'])} taxa")
        logger.debug(f"Formatted data: {formatted_data}")

        return JsonResponse(formatted_data)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)  # 添加完整的异常信息
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
def upload_custom_data(request):
    try:
        if request.method == 'POST' and request.FILES.get('file'):
            uploaded_file = request.FILES['file']
            file_type = request.POST.get('type', 'kraken')  # 获取文件类型，默认为kraken

            # 添加日志记录
            logger.info(f"Received file upload request:")
            logger.info(f"File name: {uploaded_file.name}")
            logger.info(f"File type: {file_type}")

            run_id = str(uuid.uuid4())

            # 创建目录结构
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'custom', run_id)
            os.makedirs(upload_dir, exist_ok=True)

            # 保存原始文件
            input_file = os.path.join(upload_dir, 'original_kraken.test.txt')
            with open(input_file, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # 设置输出文件路径
            output_file = os.path.join(upload_dir, f'{run_id}.compare.txt')

            # 根据文件类型选择转换脚本
            if file_type.lower() == 'kraken':
                script_name = 'kraken_to_compare.py'
            elif file_type.lower() == 'krona':
                script_name = 'krona_to_compare.py'
            else:
                logger.error(f"Unsupported file type: {file_type}")
                return JsonResponse({
                    'error': 'Unsupported file type',
                    'details': f'File type {file_type} is not supported'
                }, status=400)

            # 获取脚本路径
            script_path = os.path.join(settings.BASE_DIR, 'InsectSymbiontDB', 'scripts', script_name)

            # 记录将要执行的脚本
            logger.info(f"Using conversion script: {script_name}")

            try:
                # 添加执行权限
                os.chmod(script_path, 0o755)

                # 执行转换
                result = subprocess.run([
                    'python3', script_path, input_file, output_file
                ], check=True, capture_output=True, text=True)

                logger.info(f"File converted successfully using {script_name}")
                logger.debug(f"Conversion output: {result.stdout}")

                if not os.path.exists(output_file):
                    raise Exception("Output file was not created")

                return JsonResponse({
                    'success': True,
                    'sampleId': run_id,
                    'sampleName': uploaded_file.name,
                    'fileType': file_type
                })

            except subprocess.CalledProcessError as e:
                logger.error(f"Conversion failed using {script_name}: {str(e)}")
                logger.error(f"Script output: {e.stdout}\n{e.stderr}")
                return JsonResponse({
                    'error': 'File conversion failed',
                    'details': e.stderr
                }, status=400)

    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        return JsonResponse({
            'error': 'Upload failed',
            'details': str(e)
        }, status=400)