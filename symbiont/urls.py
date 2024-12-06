from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'symbiont'

urlpatterns = [
    path('', views.symbionts, name='symbionts'),
    path('symbiont/<int:symbiont_id>/', views.symbiont_detail, name='symbiont_detail'),
]