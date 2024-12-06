from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('', views.articles, name='articles'),
]
