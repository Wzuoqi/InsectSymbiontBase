from django.shortcuts import render, get_object_or_404
from .models import Symbiont
from django.core.paginator import Paginator
from django.db.models import Q, F
from urllib.parse import urlencode
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from article.models import Article  # 添加这行导入

# Create your views here.
def symbionts(request):
    # 获取排序参数,默认为'id'
    order_by = request.GET.get('order', 'id')

    # 确定排序方向
    if order_by.startswith('-'):
        order_field = order_by[1:]
        is_ascending = False
    else:
        order_field = order_by
        is_ascending = True

    # 获取所有Symbiont对象
    symbionts_list = Symbiont.objects.all()

    # 应用排序(包括默认排序)
    if order_by == 'id' or not order_by:
        # 由于id现在是字符串,需要特殊处理确保正确排序
        symbionts_list = symbionts_list.order_by('id')
    else:
        if is_ascending:
            symbionts_list = symbionts_list.order_by(F(order_field).asc(nulls_last=True))
        else:
            symbionts_list = symbionts_list.order_by(F(order_field).desc(nulls_last=True))

    # 处理高级搜索
    search_fields = [
        'host_order', 'host_family', 'host_species',
        'symbiont_name', 'symbiont_phylum', 'symbiont_order', 'symbiont_genus',
        'classification', 'function', 'function_tag', 'year',
        'genome_id'  # 新增genome_id搜索
    ]
    search_query = Q()
    search_params = {}

    for field in search_fields:
        value = request.GET.get(field)
        if value:
            if field == 'year':
                try:
                    year_value = int(value)
                    search_query &= Q(year=year_value)
                except ValueError:
                    continue
            else:
                search_query &= Q(**{f"{field}__icontains": value})
            search_params[field] = value

    if search_query:
        symbionts_list = symbionts_list.filter(search_query)

    # 处理快速筛选
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'bacteria':
        symbionts_list = symbionts_list.filter(classification='Bacteria')
    elif filter_type == 'fungi':
        symbionts_list = symbionts_list.filter(classification='Fungi')
    # 'all' 的情况不需要额外过滤

    # 处理普通搜索
    query = request.GET.get('q')
    if query:
        # 尝试将查询转换为年份
        try:
            year_query = int(query)
            year_condition = Q(year=year_query)
        except ValueError:
            year_condition = Q()

        symbionts_list = symbionts_list.filter(
            year_condition |
            Q(host_order__icontains=query) |
            Q(host_family__icontains=query) |
            Q(host_subfamily__icontains=query) |
            Q(host_species__icontains=query) |
            Q(symbiont_phylum__icontains=query) |
            Q(symbiont_order__icontains=query) |
            Q(symbiont_genus__icontains=query) |
            Q(symbiont_rank__icontains=query) |
            Q(symbiont_taxon__icontains=query) |
            Q(symbiont_name__icontains=query) |
            Q(classification__icontains=query) |
            Q(function__icontains=query) |
            Q(function_tag__icontains=query) |
            Q(note__icontains=query) |
            Q(journal__icontains=query) |
            Q(reference__icontains=query)
        )

    # 创建分页器对象,每页显示20条记录
    paginator = Paginator(symbionts_list, 20)

    # 获取当前页码,如果没有指定则认为第1页
    page_number = request.GET.get('page', 1)

    # 获取当前页的Page对象
    page_obj = paginator.get_page(page_number)

    # 定义标签颜色映射
    TAG_COLORS = {
        # Nutrition - 绿色系
        'Nitrogen fixation': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Feeding habits': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Probiotic': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Nutrient provision': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Digestive enzymes': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Plastic degradation': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Fungal farming': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Sugar metabolism': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',

        # Defense - 蓝色系
        'Plant defense': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Pesticide metabolization': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Immune priming': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Antimicrobials': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Plant secondary metabolites': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Natural enemy resistance': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Pathogen interaction': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Chemical biosynthesis': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',

        # Physiology - 紫色系
        'Growth and Development': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-800 dark:text-cyan-100',
        'Fertility': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-800 dark:text-cyan-100',
        'Pigmentation alteration': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-800 dark:text-cyan-100',
        'Reproductive manipulation': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-800 dark:text-cyan-100',
    }

    # 处理function_tags的拆分并添加颜色样式
    for symbiont in page_obj:
        if symbiont.function_tag and symbiont.function_tag != "NA":
            # 拆分tags并创建带颜色的tag对象
            tags_with_colors = []
            for tag in symbiont.function_tag.split(','):
                tag = tag.strip()
                if tag:
                    tags_with_colors.append({
                        'text': tag,
                        'color_class': TAG_COLORS.get(tag, 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100')  # 默认颜色
                    })
            symbiont.function_tags = tags_with_colors
        else:
            symbiont.function_tags = []

    # 构建查询参数
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = urlencode(query_params)

    # 构建上下文字典
    context = {
        'page_obj': page_obj,
        'query': query,
        'filter_type': filter_type,
        'current_order': order_by,
        'query_string': query_string,
        'search_params': json.dumps(search_params),  # 将 search_params 转换为 JSON 字符串
    }

    # 渲染模板并返回响应
    return render(request, "symbionts.html", context)

def symbionts_1(request):
    return render(request, "symbionts-1.html")

def symbiont_detail(request, symbiont_id):
    symbiont = get_object_or_404(Symbiont, id=symbiont_id)

    # 获取symbiont_name的第一个单词
    symbiont_first_word = symbiont.symbiont_name.split()[0] if symbiont.symbiont_name else ""

    # 获取相关文章 - 只使用第一个单词进行匹配
    related_articles = Article.objects.filter(
        symbiont__istartswith=symbiont_first_word
    ).order_by('-publish_time')

    # 处理字段的缺失值 - 只处理模型中存在的字段
    fields = [
        'classification', 'symbiont_phylum', 'symbiont_order', 'symbiont_genus',
        'host_order', 'host_family', 'host_subfamily', 'host_species',
        'function', 'localization', 'transmission_mode'
    ]

    for field in fields:
        value = getattr(symbiont, field)
        if value in [None, '', 'NA']:
            setattr(symbiont, field, '-')

    # 获取对应的文章信息
    if symbiont.doi and symbiont.doi != "NA":
        try:
            article = Article.objects.get(doi=symbiont.doi)
            symbiont.formatted_authors = article.formatted_authors
            symbiont.publish_year = article.publish_time
        except Article.DoesNotExist:
            symbiont.formatted_authors = None
            symbiont.publish_year = None
    else:
        symbiont.formatted_authors = None
        symbiont.publish_year = None

    # 定义标签颜色映射 (与symbionts视图保持一致)
    TAG_COLORS = {
        # Nutrition - 绿色系
        'Nitrogen fixation': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Feeding habits': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Probiotic': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Nutrient provision': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Digestive enzymes': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Plastic degradation': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Fungal farming': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',
        'Sugar metabolism': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100',

        # Defense - 蓝色系
        'Plant defense': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Pesticide metabolization': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Immune priming': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Antimicrobials': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Plant secondary metabolites': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Natural enemy resistance': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Pathogen interaction': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',
        'Chemical biosynthesis': 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-100',

        # Physiology - 紫色系
        'Growth and Development': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-800 dark:text-cyan-100',
        'Fertility': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-800 dark:text-cyan-100',
        'Pigmentation alteration': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-800 dark:text-cyan-100',
        'Reproductive manipulation': 'bg-cyan-100 text-cyan-800 dark:bg-cyan-800 dark:text-cyan-100',
    }

    # 处理function_tags (与symbionts视图保持一致的处理逻辑)
    if symbiont.function_tag and symbiont.function_tag != "NA":
        tags_with_colors = []
        for tag in symbiont.function_tag.split(','):
            tag = tag.strip()
            if tag:
                tags_with_colors.append({
                    'text': tag,
                    'color_class': TAG_COLORS.get(tag, 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100')  # 默认颜色
                })
        symbiont.function_tags = tags_with_colors
    else:
        symbiont.function_tags = []

    # 处理genome_ids
    if symbiont.genome_id and symbiont.genome_id != "NA":
        symbiont.genome_ids = [id.strip() for id in symbiont.genome_id.split(',') if id.strip()]
    else:
        symbiont.genome_ids = []

    context = {
        'symbiont': symbiont,
        'related_articles': related_articles,
    }
    return render(request, 'symbiont_detail.html', context)

@require_GET
def autocomplete(request):
    query = request.GET.get('term', '')
    if len(query) < 2:  # 只在输入至少2个字符时才返回建议
        return JsonResponse([], safe=False)

    # 从不同字段中获取建议
    suggestions = set()  # 使用集合去重

    # 限制每个字段返回的结果数量
    limit = 5

    # 从各个字段中查询匹配的值
    fields = [
        ('symbiont_name', 'Symbiont: '),
        ('host_species', 'Host: '),
        ('function_tag', 'Function: '),
        ('symbiont_phylum', 'Phylum: '),
    ]

    for field, prefix in fields:
        values = Symbiont.objects.filter(
            **{f"{field}__istartswith": query}
        ).exclude(
            **{f"{field}__in": ['', 'NA']}
        ).values_list(field, flat=True).distinct()[:limit]

        for value in values:
            if value:  # 确保值不为空
                suggestions.add(f"{prefix}{value}")

    # 转换为列表并排序
    suggestions = sorted(list(suggestions))[:10]  # 限制总建议数量为10个

    return JsonResponse(suggestions, safe=False)
