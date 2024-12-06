from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
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
        genomes = genomes.filter(source__icontains='metagenome')
    elif filter_type == 'literature_record':
        genomes = genomes.filter(source__icontains='literature')

    # 处理搜索
    query = request.GET.get('q')
    if query:
        genomes = genomes.filter(
            Q(genome_id__icontains=query) |
            Q(host__icontains=query) |
            Q(gtdb_classification__icontains=query)
        )

    # 处理高级搜索
    host = request.GET.get('host')
    completeness_min = request.GET.get('completeness_min')
    contamination_max = request.GET.get('contamination_max')
    quality_score_min = request.GET.get('quality_score_min')
    gtdb_phylum = request.GET.get('gtdb_phylum')

    if host:
        genomes = genomes.filter(host__icontains=host)
    if completeness_min:
        genomes = genomes.filter(completeness__gte=float(completeness_min))
    if contamination_max:
        genomes = genomes.filter(contamination__lte=float(contamination_max))
    if quality_score_min:
        genomes = genomes.filter(quality_score__gte=float(quality_score_min))
    if gtdb_phylum:
        genomes = genomes.filter(gtdb_phylum__icontains=gtdb_phylum)

    # 分页
    paginator = Paginator(genomes, 25)  # 每页显示25条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 准备搜索参数以供JavaScript使用
    search_params = {
        'host': host or '',
        'completeness_min': completeness_min or '',
        'contamination_max': contamination_max or '',
        'quality_score_min': quality_score_min or '',
        'gtdb_phylum': gtdb_phylum or '',
    }

    context = {
        'page_obj': page_obj,
        'query': query,
        'filter_type': filter_type,
        'current_order': order,
        'search_params': json.dumps(search_params),
        'query_string': request.GET.urlencode(),
    }

    return render(request, 'genome_catalog.html', context)

def genome_detail(request, genome_id):
    genome = get_object_or_404(Genome, id=genome_id)
    return render(request, 'genome_detail.html', {'genome': genome})
