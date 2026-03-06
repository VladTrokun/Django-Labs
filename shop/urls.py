from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('page1/', views.plants),
    path('page2/', views.about),
]