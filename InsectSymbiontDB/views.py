from django.http import HttpResponse
from django.shortcuts import render
from subprocess import Popen, PIPE
import os

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


def map(request):
    return render(request, "tools/map.html")

# def literatures(request):

#     return render(request, "literatures.html")

def host(request):
    return render(request, "host.html")


