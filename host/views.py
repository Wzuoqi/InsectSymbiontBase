from django.shortcuts import render, get_object_or_404
from .models import Host
from django.db.models import Count

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

    context = {
        'taxonomy_tree': taxonomy_tree,
        'total_species': hosts.count(),
        'total_orders': len(taxonomy_tree)
    }

    return render(request, 'hosts.html', context)

def genus_detail(request, genus_name):
    # 临时视图函数，后续可以扩展
    hosts = Host.objects.filter(genus=genus_name)
    return render(request, 'host/genus_detail.html', {
        'genus_name': genus_name,
        'hosts': hosts
    })

def species_detail(request, species_name):
    # 临时视图函数，后续可以扩展
    host = get_object_or_404(Host, species=species_name)
    return render(request, 'host/species_detail.html', {
        'host': host
    })
