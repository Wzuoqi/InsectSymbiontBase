from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Gene
from django_elasticsearch_dsl.search import Search
from elasticsearch_dsl import Q
from .documents import GeneDocument

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
        multi_match_query = Q(
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

    # 精确匹配过滤
    if source_id:
        s = s.filter('term', source_id__raw=source_id)
    if nr_id:
        s = s.filter('term', nr_id__raw=nr_id)
    if host:
        s = s.filter('term', host__raw=host)

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
