from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    # 文章列表页面
    path('', views.articles, name='articles'),
    # 文章详情页面
    path('article/<str:doi>/', views.article_detail, name='article_detail'),
]
