from django.shortcuts import render, get_object_or_404
from .models import Host
from django.db.models import Count, Q
from symbiont.models import Symbiont  # 导入Symbiont模型
from metagenome.models import Metagenome
from amplicon.models import Amplicon
from django.db.models.functions import Length
from django.db.models import Case, When, Value, IntegerField
import json
from collections import Counter
from django.db.models.functions import Substr, StrIndex

# 添加 TAG_COLORS 作为全局变量
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

# 添加排序顺序常量
INSECT_ORDER_SEQUENCE = [
    'Zygentoma',
    'Odonata',
    'Phthiraptera',
    'Dermaptera',
    'Orthoptera',
    'Phasmatodea',
    'Mantodea',
    'Blattodea',
    'Thysanoptera',
    'Hemiptera',
    'Hymenoptera',
    'Neuroptera',
    'Coleoptera',
    'Lepidoptera',
    'Diptera'
]

def hosts(request):
    # 获取所有分类数据并按层级组织
    taxonomy_tree = {}

    # 获取所有宿主数据
    hosts = Host.objects.all().order_by('order', 'family', 'genus', 'species')

    # 构建分类树
    for host in hosts:
        if host.order not in taxonomy_tree:
            taxonomy_tree[host.order] = {'families': {}, 'count': 0}

        taxonomy_tree[host.order]['count'] += 1

        # 处理 None 值，将其替换为 "Unclassified"
        family = "Unclassified" if host.family is None or host.family.lower() == 'none' else host.family

        if family not in taxonomy_tree[host.order]['families']:
            taxonomy_tree[host.order]['families'][family] = {
                'genera': {}, 'count': 0
            }

        taxonomy_tree[host.order]['families'][family]['count'] += 1

        if host.genus not in taxonomy_tree[host.order]['families'][family]['genera']:
            taxonomy_tree[host.order]['families'][family]['genera'][host.genus] = {
                'species': [], 'count': 0
            }

        taxonomy_tree[host.order]['families'][family]['genera'][host.genus]['species'].append(host)
        taxonomy_tree[host.order]['families'][family]['genera'][host.genus]['count'] += 1

    # 对 taxonomy_tree 进行排序
    sorted_taxonomy_tree = {}
    for order in INSECT_ORDER_SEQUENCE:
        if order in taxonomy_tree:
            sorted_taxonomy_tree[order] = taxonomy_tree[order]

    # 如果有其他目不在预定义序列中，将它们添加到末尾（可选）
    for order in taxonomy_tree:
        if order not in sorted_taxonomy_tree:
            sorted_taxonomy_tree[order] = taxonomy_tree[order]

    context = {
        'taxonomy_tree': sorted_taxonomy_tree,  # 使用排序后的字典
        'total_species': hosts.count(),
        'total_orders': len(taxonomy_tree)
    }

    return render(request, 'hosts.html', context)

def species_detail(request, species):
    # 获取现有的host对象
    host = get_object_or_404(Host, species=species)

    # 获取species的前两个单词用于模糊匹配
    species_words = host.species.split()[:2]
    species_pattern = ' '.join(species_words)

    # 查询相关的symbionts，添加function长度注解并排序
    related_symbionts = Symbiont.objects.filter(
        Q(host_species__istartswith=species_pattern) &
        ~Q(symbiont_name__in=['NA', 'None', '']),
    ).annotate(
        function_length=Case(
            When(function__isnull=True, then=Value(0)),
            When(function='NA', then=Value(0)),
            When(function='', then=Value(0)),
            default=Length('function'),
            output_field=IntegerField(),
        )
    ).order_by('-function_length', 'symbiont_name')  # 首先按function长度降序，然后按名称升序

    # 查询相关的metagenomes
    related_metagenomes = Metagenome.objects.filter(
        host__istartswith=species_pattern
    ).order_by('-collection_date')

    # 查询相关的amplicons
    related_amplicons = Amplicon.objects.filter(
        host__istartswith=species_pattern
    ).order_by('-collection_date')

    # 处理function_tags
    for symbiont in related_symbionts:
        if symbiont.function_tag and symbiont.function_tag not in ["NA", "", None]:
            tags_with_colors = []
            for tag in symbiont.function_tag.split(','):
                tag = tag.strip()
                if tag:
                    tags_with_colors.append({
                        'text': tag,
                        'color_class': TAG_COLORS.get(tag, 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100')
                    })
            symbiont.function_tags = tags_with_colors
        else:
            symbiont.function_tags = []

    context = {
        'host': host,
        'related_symbionts': related_symbionts,
        'related_metagenomes': related_metagenomes,
        'related_amplicons': related_amplicons,
    }

    return render(request, 'host/species_detail.html', context)


def genus_detail(request, genus_name):
    # 获取该属所属的目和科
    first_host = Host.objects.filter(genus=genus_name).first()
    order_name = first_host.order if first_host else "Unknown"
    family_name = first_host.family if first_host else "Unknown"

    # 获取该属下的所有物种
    species_list = Host.objects.filter(genus=genus_name).values_list('species', flat=True)

    # 获取该属下所有物种的前两个单词用于模糊匹配
    species_patterns = []
    for species in species_list:
        words = species.split()[:2]
        if len(words) >= 2:
            species_patterns.append(' '.join(words))

    # 使用Q对象组合多个模式的查询
    from django.db.models import Q
    species_q = Q()
    for pattern in species_patterns:
        species_q |= Q(host__istartswith=pattern)

    # 查询相关的metagenomes
    related_metagenomes = Metagenome.objects.filter(species_q).order_by('-collection_date')

    # 查询相关的amplicons
    related_amplicons = Amplicon.objects.filter(species_q).order_by('-collection_date')

    # 获取与这些物种相关的共生菌
    symbionts = Symbiont.objects.filter(
        host_species__in=species_list,
    ).filter(
        ~Q(symbiont_name__in=['NA', 'None', ''])
    ).annotate(
        function_length=Case(
            When(function__isnull=True, then=Value(0)),
            When(function='NA', then=Value(0)),
            When(function='', then=Value(0)),
            default=Length('function'),
            output_field=IntegerField(),
        )
    ).order_by('-function_length', 'symbiont_name')

    # 处理function_tags
    for symbiont in symbionts:
        if symbiont.function_tag and symbiont.function_tag not in ["NA", "", None]:
            tags_with_colors = []
            for tag in symbiont.function_tag.split(','):
                tag = tag.strip()
                if tag:
                    tags_with_colors.append({
                        'text': tag,
                        'color_class': TAG_COLORS.get(tag, 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100')
                    })
            symbiont.function_tags = tags_with_colors
        else:
            symbiont.function_tags = []

    context = {
        'genus_name': genus_name,
        'order_name': order_name,
        'family_name': family_name,
        'total_species': Host.objects.filter(genus=genus_name).count(),
        'total_symbionts': symbionts.count(),
        'hosts': Host.objects.filter(genus=genus_name).order_by('species'),
        'related_symbionts': symbionts,
        'related_metagenomes': related_metagenomes,
        'related_amplicons': related_amplicons,
    }

    return render(request, 'host/genus_detail.html', context)


def family_detail(request, family_name):
    """科详情页视图"""
    # 获取该科下的所有宿主
    hosts = Host.objects.filter(family=family_name)

    # 获取该科下的属统计
    genera = hosts.values('genus').annotate(
        species_count=Count('id')
    ).order_by('-species_count')

    # 获取该科所属的目
    order = hosts.first().order if hosts.exists() else "Unknown"

    # 查询相关的symbionts
    symbionts = Symbiont.objects.filter(
        host_family=family_name
    ).filter(
        ~Q(symbiont_name__in=['NA', 'None', ''])
    ).annotate(
        function_length=Case(
            When(function__isnull=True, then=Value(0)),
            When(function='NA', then=Value(0)),
            When(function='', then=Value(0)),
            default=Length('function'),
            output_field=IntegerField(),
        )
    ).order_by('-function_length', 'symbiont_name')

    # 查询相关的metagenomes
    related_metagenomes = Metagenome.objects.filter(
        host_family=family_name
    ).order_by('-collection_date')

    # 查询相关的amplicons
    related_amplicons = Amplicon.objects.filter(
        host_family=family_name
    ).order_by('-collection_date')

    # 处理function_tags
    for symbiont in symbionts:
        if symbiont.function_tag and symbiont.function_tag not in ["NA", "", None]:
            tags_with_colors = []
            for tag in symbiont.function_tag.split(','):
                tag = tag.strip()
                if tag:
                    tags_with_colors.append({
                        'text': tag,
                        'color_class': TAG_COLORS.get(tag, 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100')
                    })
            symbiont.function_tags = tags_with_colors
        else:
            symbiont.function_tags = []

    context = {
        'family_name': family_name,
        'order_name': order,
        'total_species': hosts.count(),
        'total_genera': len(genera),
        'genera': genera,
        'total_symbionts': symbionts.count(),
        'hosts': hosts.order_by('genus', 'species'),
        'related_symbionts': symbionts,
        'related_metagenomes': related_metagenomes,
        'related_amplicons': related_amplicons,
    }

    return render(request, 'host/family_detail.html', context)

def order_detail(request, order_name):
    """目详情页视图"""
    # 获取该目下的所有宿主
    hosts = Host.objects.filter(order=order_name)

    # 获取该目下的科统计
    families = hosts.values('family').annotate(
        species_count=Count('id')
    ).order_by('-species_count')

    # 查询相关的symbionts
    symbionts = Symbiont.objects.filter(
        host_order=order_name
    ).filter(
        ~Q(symbiont_name__in=['NA', 'None', ''])
    ).annotate(
        function_length=Case(
            When(function__isnull=True, then=Value(0)),
            When(function='NA', then=Value(0)),
            When(function='', then=Value(0)),
            default=Length('function'),
            output_field=IntegerField(),
        )
    ).order_by('-function_length', 'symbiont_name')

    # 查询相关的metagenomes
    related_metagenomes = Metagenome.objects.filter(
        host_order=order_name
    ).order_by('-collection_date')

    # 查询相关的amplicons
    related_amplicons = Amplicon.objects.filter(
        host_order=order_name
    ).order_by('-collection_date')

    # 处理function_tags
    for symbiont in symbionts:
        if symbiont.function_tag and symbiont.function_tag not in ["NA", "", None]:
            tags_with_colors = []
            for tag in symbiont.function_tag.split(','):
                tag = tag.strip()
                if tag:
                    tags_with_colors.append({
                        'text': tag,
                        'color_class': TAG_COLORS.get(tag, 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-100')
                    })
            symbiont.function_tags = tags_with_colors
        else:
            symbiont.function_tags = []

    context = {
        'order_name': order_name,
        'total_species': hosts.count(),
        'total_families': len(families),
        'families': families,
        'total_symbionts': symbionts.count(),
        'hosts': hosts.order_by('family', 'genus', 'species'),
        'related_symbionts': symbionts,
        'related_metagenomes': related_metagenomes,
        'related_amplicons': related_amplicons,
    }

    return render(request, 'host/order_detail.html', context)
