from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'gene'

urlpatterns = [
    path('', views.genes, name='genes'),
    path('gene/<str:source_id>/<str:gene_id>/', views.gene_detail, name='gene_detail'),
]
