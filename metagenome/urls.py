from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'metagenome'

urlpatterns = [
    path('', views.metagenomes, name='metagenomes'),
    path('metagenome/<int:metagenome_id>/', views.metagenome_detail, name='metagenome_detail'),
]
