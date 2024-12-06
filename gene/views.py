from django.shortcuts import render
from django.db.models import Q  # 直接导入Q用于搜索过滤
from .models import Gene  # 导入gene模型

def genes(request):
    return render(request, 'gene_catalog.html')

def gene_detail(request):
    return render(request, 'gene_catalog.html')