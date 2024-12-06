from django.shortcuts import render, get_object_or_404
from .models import Metagenome
from django.core.paginator import Paginator
from django.db.models import Q

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
    paginator = Paginator(metagenomes_list, 10)

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

def metagenome_detail(request, metagenome_id):
    metagenome = get_object_or_404(Metagenome, id=metagenome_id)
    context = {
        'metagenome': metagenome,
    }
    return render(request, 'metagenome_detail.html', context)