from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('plants/', views.plants),
    path('about/', views.about),
]