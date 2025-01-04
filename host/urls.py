from django.urls import path, re_path
from . import views

app_name = 'host'

urlpatterns = [
    path('', views.hosts, name='hosts'),
    path('order/<str:order_name>/', views.order_detail, name='order_detail'),
    path('family/<str:family_name>/', views.family_detail, name='family_detail'),
    path('genus/<str:genus_name>/', views.genus_detail, name='genus_detail'),
    path('species/<str:species>/', views.species_detail, name='species_detail'),
]
