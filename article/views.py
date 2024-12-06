from django.shortcuts import render
from django.db.models import Q  # 直接导入Q用于搜索过滤
from .models import Article  # 导入Article模型

def articles(request):
    query = request.GET.get('q', '')  # 获取查询参数
    if query:
        # 搜索所有字段
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(authors__icontains=query) |
            Q(journal__icontains=query) |
            Q(doi__icontains=query) |
            Q(wos__icontains=query) |
            Q(species__icontains=query)
        )
    else:
        articles = Article.objects.all()

    context = {'articles': articles}
    return render(request, 'article/articles.html', context)