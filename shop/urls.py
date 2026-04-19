from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('plants/', views.plants, name='plants'),
    path('about/', views.about, name='about'),
    # Нові маршрути:
    path('plant/<int:pk>/', views.plant_detail, name='plant_detail'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
]