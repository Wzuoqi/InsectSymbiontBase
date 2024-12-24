from django.urls import path
from . import views

app_name = 'host'

urlpatterns = [
    path('', views.hosts, name='hosts'),
    path('genus/<str:genus_name>/', views.genus_detail, name='genus_detail'),
    path('species/<str:species_name>/', views.species_detail, name='species_detail'),
]
