from django.shortcuts import render, get_object_or_404
from .models import Symbiont
from django.core.paginator import Paginator
from django.db.models import Q, F, Case, When, Value, IntegerField
from urllib.parse import urlencode
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from article.models import Article  # 添加这行导入
from genome.models import Genome  # 添加这行导入

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
            Q(id__icontains=query) |
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

def expand_accession_range(start, end):
    """展开类似HM222405-HM222408这样的序列号范围"""
    # 提取前缀和数字部分
    prefix = ''.join(c for c in start if not c.isdigit())
    start_num = int(''.join(c for c in start if c.isdigit()))
    end_num = int(''.join(c for c in end if c.isdigit()))

    # 生成范围内的所有序列号
    return [f"{prefix}{str(num).zfill(len(str(start_num)))}"
            for num in range(start_num, end_num + 1)]

def process_accession_numbers(accession_str):
    """处理序列号字符串，返回分类后的序列号字典"""
    if not accession_str or accession_str == 'NA' or accession_str == '-':
        return {}

    # 存储不同类型的序列号
    accession_dict = {
        'Assembly': [],
        'GenBank': [],
        'SRA': [],
        'Bioproject': [],
        'Other': []
    }

    # 首先按逗号分割
    parts = [p.strip() for p in accession_str.split(',')]

    for part in parts:
        # 检查是否是范围表示
        if '-' in part:
            start, end = [p.strip() for p in part.split('-')]
            numbers = expand_accession_range(start, end)
        else:
            numbers = [part]

        # 对每个序列号进行分类
        for number in numbers:
            number = number.strip()

            # 使用正则表达式匹配不同格式
            # Assembly (GCA开头)
            if number.startswith('GCA'):
                accession_dict['Assembly'].append(number)

            # GenBank (两个字母开头+数字)
            elif (len(number) >= 3 and
                  number[:2].isalpha() and
                  not number[:2].startswith('PR') and  # 排除PRJ开头的
                  len(number) >= 3 and
                  number[2:].replace('_', '').isdigit()):
                accession_dict['GenBank'].append(number)

            # SRA (三个字母开头+数字，第二个字母为R)
            elif (len(number) >= 4 and
                  number[:3].isalpha() and
                  number[1].upper() == 'R' and
                  number[3:].replace('_', '').isdigit()):
                accession_dict['SRA'].append(number)

            # Bioproject (PRJ开头)
            elif number.startswith('PRJ'):
                accession_dict['Bioproject'].append(number)

            # 其他
            else:
                accession_dict['Other'].append(number)

    # 移除空列表并排序
    return {k: sorted(v) for k, v in accession_dict.items() if v}

def symbiont_detail(request, symbiont_id):
    symbiont = get_object_or_404(Symbiont, id=symbiont_id)

    # 获取symbiont_name的第一个单词
    symbiont_first_word = symbiont.symbiont_name.split()[0] if symbiont.symbiont_name else ""

    # 获取host_species的前两个单词
    host_species_words = symbiont.host_species.split()[:2] if symbiont.host_species else []
    host_species_pattern = ' '.join(host_species_words) if host_species_words else ""

    # 分别获取两种匹配的结果
    symbiont_matches = set(Article.objects.filter(
        symbiont__istartswith=symbiont_first_word
    ).values_list('id', flat=True))

    host_matches = set(Article.objects.filter(
        species__istartswith=host_species_pattern
    ).values_list('id', flat=True))

    # 获取同时匹配的文章ID
    both_matches = symbiont_matches & host_matches

    # 获取所有相关文章并添加排序字段
    related_articles = Article.objects.filter(
        id__in=symbiont_matches | host_matches
    ).annotate(
        match_score=Case(
            When(id__in=both_matches, then=Value(2)),  # 同时匹配得分最高
            When(id__in=symbiont_matches, then=Value(1)),  # 仅匹配symbiont次之
            When(id__in=host_matches, then=Value(1)),  # 仅匹配host同样
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('-match_score', '-publish_time')  # 首先按匹配分数排序，然后按发表时间

    # 为每篇文章添加匹配标记
    for article in related_articles:
        article.matched_by_symbiont = article.id in symbiont_matches
        article.matched_by_host = article.id in host_matches

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
        genome_ids = [id.strip() for id in symbiont.genome_id.split(',') if id.strip()]
        # 获取每个 genome_id 对应的 Genome 对象
        genome_objects = []
        for gid in genome_ids:
            try:
                genome = Genome.objects.get(genome_id=gid)
                genome_objects.append({
                    'id': gid,
                    'symbiont_name': genome.symbiont_name
                })
            except Genome.DoesNotExist:
                genome_objects.append({
                    'id': gid,
                    'symbiont_name': None
                })
        symbiont.genome_ids = genome_objects
    else:
        symbiont.genome_ids = []

    # 处理related_accession
    if symbiont.related_accession and symbiont.related_accession != "NA":
        symbiont.processed_accessions = process_accession_numbers(symbiont.related_accession)
    else:
        symbiont.processed_accessions = {}

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
