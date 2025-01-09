from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Genome
import json

def genomes(request):
    # 获取所有基因组
    genomes = Genome.objects.all()

    # 处理排序
    order = request.GET.get('order', 'genome_id')
    if order.startswith('-'):
        genomes = genomes.order_by(order)
    else:
        genomes = genomes.order_by(order)

    # 处理过滤
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'metagenome_mags':
        genomes = genomes.filter(source__icontains='Metagenome MAGs')
    elif filter_type == 'literature_record':
        genomes = genomes.filter(source__icontains='Literature Record')
    elif filter_type == 'public_database':  # 添加新的过滤选项
        genomes = genomes.filter(source__icontains='Public Database')

    # 处理搜索
    query = request.GET.get('q')
    if query:
        genomes = genomes.filter(
            Q(genome_id__icontains=query) |
            Q(source_id__icontains=query) |
            Q(host__icontains=query) |
            Q(reference_name__icontains=query) |
            Q(reference_phylum__icontains=query) |
            Q(gtdb_classification__icontains=query) |
            Q(function__icontains=query)
        )

    # 处理高级搜索
    genome_id = request.GET.get('genome_id')
    source_id = request.GET.get('source_id')
    host = request.GET.get('host')
    source = request.GET.get('source')
    completeness_min = request.GET.get('completeness_min')
    contamination_max = request.GET.get('contamination_max')
    gtdb_phylum = request.GET.get('gtdb_phylum')
    gtdb_class = request.GET.get('gtdb_class')

    if genome_id:
        genomes = genomes.filter(genome_id__icontains=genome_id)
    if source_id:
        genomes = genomes.filter(source_id__icontains=source_id)
    if host:
        genomes = genomes.filter(host__icontains=host)
    if source:
        genomes = genomes.filter(source=source)
    if completeness_min:
        try:
            genomes = genomes.filter(completeness__gte=float(completeness_min))
        except ValueError:
            pass
    if contamination_max:
        try:
            genomes = genomes.filter(contamination__lte=float(contamination_max))
        except ValueError:
            pass
    if gtdb_phylum:
        genomes = genomes.filter(gtdb_classification__icontains=gtdb_phylum)
    if gtdb_class:
        genomes = genomes.filter(gtdb_classification__icontains=gtdb_class)

    # 获取所有的GET参数
    search_params = request.GET.copy()
    if 'page' in search_params:
        del search_params['page']

    # 分页处理
    paginator = Paginator(genomes, 25)  # 每页显示25条记录
    page = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 准备查询字符串（用于分页）
    query_dict = request.GET.copy()
    if 'page' in query_dict:
        del query_dict['page']
    query_string = query_dict.urlencode()

    # 构建上下文字典
    context = {
        'page_obj': page_obj,
        'query': query,
        'filter_type': filter_type,
        'current_order': order,
        'search_params': search_params.urlencode() if search_params else '{}',
        'query_string': query_string,
    }

    return render(request, 'genome_catalog.html', context)

def genome_detail(request, genome_id):
    genome = get_object_or_404(Genome, genome_id=genome_id)
    context = {
        'genome': genome,
    }
    return render(request, 'genome_detail.html', context)