from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'metagenome'

urlpatterns = [
    path('', views.metagenomes, name='metagenomes'),
    path('metagenome/<str:run>/', views.metagenome_detail, name='metagenome_detail'),
]
