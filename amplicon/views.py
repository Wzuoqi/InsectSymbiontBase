from django.shortcuts import render, get_object_or_404
from .models import Amplicon
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

# Create your views here.

def format_collection_date(date_str):
    """
    Convert various date formats to year
    """
    if not date_str or date_str == "NA":
        return None

    try:
        # 尝试将字符串转换为整数
        date_num = int(date_str)

        # 如果是合理的年份范围（1900-2024）
        if 1900 <= date_num <= 2024:
            return str(date_num)

        # 如果是两位数年份（如70表示1970）
        if 0 <= date_num <= 99:
            year = 1900 + date_num
            return str(year) if year <= 2024 else None

        # 如果是Unix时间戳
        if date_num > 10000:  # 假设大于10000的是时间戳
            try:
                year = datetime.fromtimestamp(date_num).year
                return str(year) if 1900 <= year <= 2024 else None
            except ValueError:
                return None

    except ValueError:
        # 如果不是数字，尝试其他日期格式
        try:
            # 尝试解析常见的日期格式
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y']:
                try:
                    year = datetime.strptime(date_str, fmt).year
                    return str(year) if 1900 <= year <= 2024 else None
                except ValueError:
                    continue
        except:
            return None

    return None

def amplicons(request):
    # Get all Amplicon objects
    amplicons_list = Amplicon.objects.all()

    # Handle quick filter
    filter_type = request.GET.get('filter', 'all')
    if filter_type == '16s':
        amplicons_list = amplicons_list.filter(classification='16S')
    elif filter_type == 'others':
        amplicons_list = amplicons_list.exclude(classification='16S')

    # Define search fields
    search_fields = ['run', 'assay_type', 'biosample', 'center_name', 'instrument', 'library_layout', 'bioproject', 'classification', 'geo_loc_name_country', 'geo_loc_name_country_continent', 'geo_loc_name', 'host', 'env_broad_scale', 'env_local_scale', 'env_medium', 'host_sex']

    # Handle advanced search
    query = Q()
    for field in search_fields:
        value = request.GET.get(field)
        if value:
            query &= Q(**{f"{field}__icontains": value})

    # Handle basic search
    search_query = request.GET.get('search', '')
    if search_query:
        basic_query = Q()
        for field in search_fields:
            basic_query |= Q(**{f"{field}__icontains": search_query})
        query &= basic_query

    amplicons_list = amplicons_list.filter(query)

    # Handle sorting
    sort_by = request.GET.get('sort_by', 'run')
    if sort_by not in ['run', 'host', 'geo_loc_name_country', 'collection_date']:
        sort_by = 'run'
    amplicons_list = amplicons_list.order_by(sort_by)

    # Pagination
    paginator = Paginator(amplicons_list, 20)  # Show 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取所有的GET参数
    search_params = request.GET.copy()
    if 'page' in search_params:
        del search_params['page']

    # 在构建context之前添加日期处理
    for amplicon in page_obj:
        if amplicon.collection_date:
            formatted_date = format_collection_date(amplicon.collection_date)
            amplicon.formatted_year = formatted_date or 'Invalid date'

    # 构建上下文字典
    context = {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'search_query': search_query,
        'filter_type': filter_type,
        'search_params': search_params.urlencode() if search_params else '{}',
    }

    return render(request, "amplicons.html", context)

def amplicon_detail(request, run):
    amplicon = get_object_or_404(Amplicon, run=run)
    context = {
        'amplicon': amplicon,
    }
    return render(request, 'amplicon_detail.html', context)
