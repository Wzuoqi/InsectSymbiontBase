from django.shortcuts import render, get_object_or_404
from .models import Metagenome
from django.core.paginator import Paginator
from django.db.models import Q
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def metagenomes(request):
    # 获取所有Metagenome对象
    metagenomes_list = Metagenome.objects.all()

    # 处理高级搜索
    search_fields = ['run', 'assay_type', 'biosample', 'center_name', 'instrument', 'library_layout', 'library_selection', 'platform', 'bioproject', 'geo_loc_name_country', 'geo_loc_name_country_continent', 'geo_loc_name', 'biosample_model', 'lat_lon', 'host']
    search_query = Q()
    for field in search_fields:
        value = request.GET.get(field)
        if value:
            search_query &= Q(**{f"{field}__icontains": value})

    if search_query:
        metagenomes_list = metagenomes_list.filter(search_query)

    # 处理快速筛选
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'wgs':
        metagenomes_list = metagenomes_list.filter(assay_type='WGS')
    elif filter_type == 'amplicon':
        metagenomes_list = metagenomes_list.exclude(assay_type='WGS')

    # 处理普通搜索
    query = request.GET.get('q')
    if query:
        metagenomes_list = metagenomes_list.filter(
            Q(run__icontains=query) |
            Q(assay_type__icontains=query) |
            Q(biosample__icontains=query) |
            Q(center_name__icontains=query) |
            Q(instrument__icontains=query) |
            Q(platform__icontains=query) |
            Q(bioproject__icontains=query) |
            Q(geo_loc_name_country__icontains=query) |
            Q(geo_loc_name_country_continent__icontains=query) |
            Q(geo_loc_name__icontains=query) |
            Q(biosample_model__icontains=query) |
            Q(host__icontains=query)
        )

    # 创建分页器对象,每页显示10条记录
    paginator = Paginator(metagenomes_list, 25)

    # 获取当前页码,如果没有指定则默认为第1页
    page_number = request.GET.get('page', 1)

    # 获取当前页的Page对象
    page_obj = paginator.get_page(page_number)

    # 获取所有的GET参数
    search_params = request.GET.copy()
    if 'page' in search_params:
        del search_params['page']

    # 构建上下文字典
    context = {
        'page_obj': page_obj,
        'query': query,
        'filter_type': filter_type,
        'search_params': search_params.urlencode(),  # 添加这行
    }

    # 渲染模板并返回响应
    return render(request, "metagenomes.html", context)

def metagenomes_1(request):
    return render(request, "metagenomes-1.html")

def metagenome_detail(request, run):
    metagenome = get_object_or_404(Metagenome, run=run)

    # 读取symbiont数据
    symbionts = []
    symbiont_file = os.path.join(settings.MEDIA_ROOT, 'metagenome', 'symbiont_from_meta.txt')

    if os.path.exists(symbiont_file):
        with open(symbiont_file, 'r') as f:
            # 跳过标题行
            next(f)
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 11:
                    symbiont = {
                        'percentage': float(parts[0]),
                        'name': parts[1],
                        'db_id': parts[2],
                        'order': parts[3],
                        'insect_species': parts[4],
                        'genus': parts[5],
                        'species': parts[6],
                        'function': parts[7],
                        'species_match': parts[8] == 'True',
                        'order_match': parts[9] == 'True',
                        'total_score': float(parts[10])
                    }
                    symbionts.append(symbiont)

        # 按总分排序
        symbionts.sort(key=lambda x: x['total_score'], reverse=True)

    return render(request, 'metagenome_detail.html', {
        'metagenome': metagenome,
        'symbionts': symbionts
    })

@require_GET
def autocomplete(request):
    query = request.GET.get('term', '')
    if len(query) < 2:
        return JsonResponse([], safe=False)

    # 从不同字段中获取建议
    suggestions = set()
    limit = 5

    # 简化搜索字段，只保留最重要的几个
    fields = [
        ('host', 'Host'),
        ('geo_loc_name_country', 'Country'),
        ('geo_loc_name', 'Location'),
        ('platform', 'Platform')
    ]

    for field, prefix in fields:
        # 使用 startswith 而不是 icontains
        values = Metagenome.objects.filter(
            **{f"{field}__istartswith": query}
        ).exclude(
            **{f"{field}__exact": ''},
            **{f"{field}__exact": 'NA'}
        ).values_list(field, flat=True).distinct()[:limit]

        for value in values:
            if value:
                suggestions.add(f"{prefix}: {value}")

    # 转换为列表并排序
    suggestions = sorted(list(suggestions))[:10]

    return JsonResponse(suggestions, safe=False)
