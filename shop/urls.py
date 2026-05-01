from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- Основні сторінки магазину ---
    path('', views.home, name='home'),
    path('plants/', views.plants, name='plants'),
    path('about/', views.about, name='about'),
    path('top-plants/', views.top_plants, name='top_plants'),
    path('plant/<int:pk>/', views.plant_detail, name='plant_detail'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),

    # --- Кошик та замовлення ---
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add-to-cart/<int:plant_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-single/<int:plant_id>/', views.remove_single_from_cart, name='remove_single_from_cart'),
    path('remove-from-cart/<int:plant_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # --- Нова Пошта API ---
    path('api/np/cities/', views.np_search_cities, name='np_search_cities'),
    path('api/np/warehouses/', views.np_get_warehouses, name='np_get_warehouses'),

    # --- Розсилка ---
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),

    # --- Акаунти ---
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),

    # --- Вхід / Вихід ---
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True,
    ), name='login'),

    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='home',
    ), name='logout'),

    # --- Зміна паролю (залогінений) ---
    path('accounts/password-change/', auth_views.PasswordChangeView.as_view(
        template_name='password_change_form.html',
        success_url='/accounts/password-change/done/',
    ), name='password_change'),

    path('accounts/password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html',
    ), name='password_change_done'),

    # --- Відновлення паролю через email ---
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        success_url='/accounts/password-reset/done/',
    ), name='password_reset'),

    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html',
    ), name='password_reset_done'),

    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url='/accounts/password-reset/complete/',
    ), name='password_reset_confirm'),

    path('accounts/password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html',
    ), name='password_reset_complete'),
]