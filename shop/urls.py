from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('plants/', views.plants, name='plants'),
    path('about/', views.about, name='about'),
    path('plant/<int:pk>/', views.plant_detail, name='plant_detail'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:plant_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-single/<int:plant_id>/', views.remove_single_from_cart, name='remove_single_from_cart'),
    path('remove-from-cart/<int:plant_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('top-plants/', views.top_plants, name='top_plants'),
    path('checkout/', views.checkout, name='checkout'),
]