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
    search_fields = [
        'run', 'assay_type', 'biosample', 'center_name', 'instrument',
        'library_layout', 'library_selection', 'platform', 'bioproject',
        'geo_loc_name_country', 'geo_loc_name_country_continent',
        'geo_loc_name', 'biosample_model', 'host'
    ]

    search_query = Q()
    for field in search_fields:
        value = request.GET.get(field)
        if value:
            # 对于地理位置字段进行特殊处理，支持冒号分隔的格式
            if field == 'geo_loc_name':
                locations = value.split(':')
                loc_query = Q()
                for loc in locations:
                    loc = loc.strip()
                    if loc:
                        loc_query |= Q(geo_loc_name__icontains=loc)
                search_query &= loc_query
            else:
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
        basic_query = Q()
        for field in search_fields:
            # 对于地理位置字段进行特殊处理
            if field == 'geo_loc_name':
                locations = query.split(':')
                for loc in locations:
                    loc = loc.strip()
                    if loc:
                        basic_query |= Q(geo_loc_name__icontains=loc)
            else:
                basic_query |= Q(**{f"{field}__icontains": query})
        metagenomes_list = metagenomes_list.filter(basic_query)

    # 创建分页器对象,每页显示25条记录
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
        'search_params': search_params.urlencode() if search_params else '{}',
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
                # 确保有足够的字段（现在需要12个字段，因为新增了insect_match）
                if len(parts) >= 12:
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
                        'insect_match': parts[10] == 'True',  # 新增字段
                        'total_score': float(parts[11])       # 总分的位置变更
                    }
                    symbionts.append(symbiont)

        # 按总分排序
        symbionts.sort(key=lambda x: x['total_score'], reverse=True)

    return render(request, 'metagenome_detail.html', {
        'metagenome': metagenome,
        'symbionts': symbionts
    })
