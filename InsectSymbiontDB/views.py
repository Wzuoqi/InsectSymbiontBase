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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
        print("Received POST request") # 调试日志

        try:
            # 获取表单数据
            host_order = request.POST.get('host_order')
            host_name = request.POST.get('host_name')

            print(f"Host Order: {host_order}") # 调试日志
            print(f"Host Name: {host_name}") # 调试日志

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

                # 进行物种级别的比对
                species_matches = match_species_level(input_file_path, symbiont_db)
                print(f"Found {len(species_matches)} species matches") # 调试日志

                # 进行属级别的比对
                genus_matches = match_genus_level(input_file_path, symbiont_db)
                print(f"Found {len(genus_matches)} genus matches") # 调试日志

                # 过滤属级别的匹配结果
                filtered_genus_matches = filter_genus_matches(species_matches, genus_matches)

                # 合并所有匹配结果
                all_matches = species_matches + filtered_genus_matches

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

# def literatures(request):

#     return render(request, "literatures.html")

def hosts(request):
    return render(request, "hosts.html")

def contact(request):
    return render(request, "contact.html")

def help(request):
    return render(request, "help.html")