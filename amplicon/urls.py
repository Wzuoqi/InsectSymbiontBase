from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

app_name = 'amplicon'

urlpatterns = [
    path('', views.amplicons, name='amplicons'),
    path('amplicon/<str:run>/', views.amplicon_detail, name='amplicon_detail'),
]
