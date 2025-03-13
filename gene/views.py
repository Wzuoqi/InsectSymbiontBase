from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Gene
from elasticsearch_dsl import Q as ESQ
from .documents import GeneDocument
import csv
from django.http import HttpResponse
import datetime

def genes(request):
    # 获取搜索参数
    query = request.GET.get('query', '').strip()
    source_id = request.GET.get('source_id', '').strip()
    nr_id = request.GET.get('nr_id', '').strip()
    nr_annotation = request.GET.get('nr_annotation', '').strip()
    host = request.GET.get('host', '').strip()
    go_terms = request.GET.get('go_terms', '').strip()
    kegg_ko = request.GET.get('kegg_ko', '').strip()
    kegg_pathway = request.GET.get('kegg_pathway', '').strip()
    pfams = request.GET.get('pfams', '').strip()

    # 构建基础查询
    s = GeneDocument.search()

    # 添加调试日志
    print(f"Search query: {query}")

    # 基础多字段搜索
    if query:
        multi_match_query = ESQ(
            'multi_match',
            query=query,
            fields=[
                'nr_annotation^3',  # 给予更高权重
                'description^3',
                'preferred_name^2',
                'nr_species',
                'go_terms',
                'kegg_pathway',
                'pfams'
            ],
            type='best_fields',
            operator='or',  # 改为 or 使搜索更宽松
            minimum_should_match='50%'  # 降低匹配要求
        )
        s = s.query(multi_match_query)

        # 添加调试日志
        print(f"Elasticsearch query: {s.to_dict()}")

    # 修改为使用模糊匹配而不是精确匹配
    if source_id:
        s = s.query('wildcard', source_id=f"*{source_id}*")
    if nr_id:
        s = s.query('wildcard', nr_id=f"*{nr_id}*")
    if host:
        s = s.query('wildcard', host=f"*{host}*")

    # 模糊匹配过滤
    if nr_annotation:
        s = s.query('match', nr_annotation=nr_annotation)
    if go_terms:
        s = s.query('match', go_terms=go_terms)
    if kegg_ko:
        s = s.query('match', kegg_ko=kegg_ko)
    if kegg_pathway:
        s = s.query('match', kegg_pathway=kegg_pathway)
    if pfams:
        s = s.query('match', pfams=pfams)

    # 分页
    page = request.GET.get('page', 1)
    per_page = 20
    start = (int(page) - 1) * per_page
    end = start + per_page

    # 执行搜索并添加调试信息
    try:
        total = s.count()
        print(f"Total results: {total}")
        search_results = s[start:end].execute()
        print(f"Results returned: {len(search_results)}")
    except Exception as e:
        print(f"Search error: {str(e)}")
        total = 0
        search_results = []

    # 构建分页器
    paginator = Paginator(range(total), per_page)
    page_obj = paginator.get_page(page)

    context = {
        'genes': search_results,
        'page_obj': page_obj,
        'query': query,
        'source_id': source_id,
        'nr_id': nr_id,
        'nr_annotation': nr_annotation,
        'host': host,
        'go_terms': go_terms,
        'kegg_ko': kegg_ko,
        'kegg_pathway': kegg_pathway,
        'pfams': pfams,
        'total_count': total,
    }

    return render(request, 'gene_catalog.html', context)

def gene_detail(request, source_id, gene_id):
    gene = get_object_or_404(Gene, source_id=source_id, gene_id=gene_id)
    return render(request, 'gene_detail.html', {'gene': gene})

def download_genes(request):
    """
    下载基因搜索结果为TSV文件
    """
    # 获取搜索参数 (与 genes 视图相同)
    query = request.GET.get('query', '').strip()
    source_id = request.GET.get('source_id', '').strip()
    nr_id = request.GET.get('nr_id', '').strip()
    nr_annotation = request.GET.get('nr_annotation', '').strip()
    host = request.GET.get('host', '').strip()
    go_terms = request.GET.get('go_terms', '').strip()
    kegg_ko = request.GET.get('kegg_ko', '').strip()
    kegg_pathway = request.GET.get('kegg_pathway', '').strip()
    pfams = request.GET.get('pfams', '').strip()

    # 构建与搜索页面相同的查询
    s = GeneDocument.search()

    # 基础多字段搜索
    if query:
        multi_match_query = ESQ(
            'multi_match',
            query=query,
            fields=[
                'nr_annotation^3',
                'description^3',
                'preferred_name^2',
                'nr_species',
                'go_terms',
                'kegg_pathway',
                'pfams'
            ],
            type='best_fields',
            operator='or',
            minimum_should_match='50%'
        )
        s = s.query(multi_match_query)

    # 使用通配符查询进行部分匹配
    if source_id:
        s = s.query('wildcard', source_id=f"*{source_id}*")
    if nr_id:
        s = s.query('wildcard', nr_id=f"*{nr_id}*")
    if host:
        s = s.query('wildcard', host=f"*{host}*")

    # 模糊匹配过滤
    if nr_annotation:
        s = s.query('match', nr_annotation=nr_annotation)
    if go_terms:
        s = s.query('match', go_terms=go_terms)
    if kegg_ko:
        s = s.query('match', kegg_ko=kegg_ko)
    if kegg_pathway:
        s = s.query('match', kegg_pathway=kegg_pathway)
    if pfams:
        s = s.query('match', pfams=pfams)

    # 设置较大的 size 值，但有上限以避免内存问题
    # 注意：如果结果超过此限制，应考虑使用 scroll API
    max_size = 10000
    total = s.count()
    download_size = min(total, max_size)

    # 获取搜索结果
    search_results = s[0:download_size].execute()

    # 创建 HTTP 响应，设置为 TSV 文件
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    response = HttpResponse(content_type='text/tab-separated-values')
    response['Content-Disposition'] = f'attachment; filename="gene_search_results_{timestamp}.tsv"'

    # 创建 TSV writer
    writer = csv.writer(response, delimiter='\t')

    # 写入表头
    headers = [
        'host', 'source_id', 'gene_id', 'nr_id', 'identity',
        'alignment_length', 'mismatches', 'gap_openings',
        'query_start', 'query_end', 'subject_start', 'subject_end',
        'evalue', 'bit_score', 'gene_length', 'nr_annotation',
        'nr_species', 'seed_ortholog', 'description', 'preferred_name',
        'go_terms', 'ec_number', 'kegg_ko', 'kegg_pathway', 'pfams'
    ]
    writer.writerow(headers)

    # 写入数据行
    for gene in search_results:
        row = [
            getattr(gene, 'host', ''),
            getattr(gene, 'source_id', ''),
            getattr(gene, 'gene_id', ''),
            getattr(gene, 'nr_id', ''),
            getattr(gene, 'identity', ''),
            getattr(gene, 'alignment_length', ''),
            getattr(gene, 'mismatches', ''),
            getattr(gene, 'gap_openings', ''),
            getattr(gene, 'query_start', ''),
            getattr(gene, 'query_end', ''),
            getattr(gene, 'subject_start', ''),
            getattr(gene, 'subject_end', ''),
            getattr(gene, 'evalue', ''),
            getattr(gene, 'bit_score', ''),
            getattr(gene, 'gene_length', ''),
            getattr(gene, 'nr_annotation', ''),
            getattr(gene, 'nr_species', ''),
            getattr(gene, 'seed_ortholog', ''),
            getattr(gene, 'description', ''),
            getattr(gene, 'preferred_name', ''),
            getattr(gene, 'go_terms', ''),
            getattr(gene, 'ec_number', ''),
            getattr(gene, 'kegg_ko', ''),
            getattr(gene, 'kegg_pathway', ''),
            getattr(gene, 'pfams', '')
        ]
        writer.writerow(row)

    # 添加下载信息
    if total > max_size:
        info_row = [f"Note: Only {max_size} of {total} total results are included in this download."]
        writer.writerow([])
        writer.writerow(info_row)

    return response
