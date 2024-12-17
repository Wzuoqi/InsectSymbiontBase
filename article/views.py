from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article

def articles(request):
    # 获取所有文章
    articles_list = Article.objects.all()

    # 处理搜索
    search_query = request.GET.get('q', '')
    if search_query:
        articles_list = articles_list.filter(
            Q(title__icontains=search_query) |
            Q(authors__icontains=search_query) |
            Q(journal__icontains=search_query) |
            Q(species__icontains=search_query) |
            Q(symbiont__icontains=search_query)
        )

    # 排序
    sort_by = request.GET.get('sort', 'id')  # 默认按发布时间降序
    articles_list = articles_list.order_by(sort_by)

    # 分页 - 每页显示25篇文章
    paginator = Paginator(articles_list, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 计算显示的页码范围
    page_range = get_page_range(page_obj.number, paginator.num_pages)

    context = {
        'articles': page_obj,
        'page_obj': page_obj,
        'page_range': page_range,
        'search_query': search_query,
        'total_count': articles_list.count(),
    }
    return render(request, 'article/articles.html', context)

def get_page_range(current_page, total_pages, window=5):
    """计算要显示的页码范围"""
    half_window = window // 2
    start_page = max(current_page - half_window, 1)
    end_page = min(current_page + half_window, total_pages)

    if current_page <= half_window:
        end_page = min(window, total_pages)
    elif current_page >= total_pages - half_window:
        start_page = max(total_pages - window + 1, 1)

    return range(start_page, end_page + 1)