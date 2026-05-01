from django.contrib import admin
from .models import Category, Plant, Order, OrderItem, Review, Newsletter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('plant', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Поля які реально є на моделі Order
    list_display = ('id', 'user', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('total_price', 'created_at')
    inlines = [OrderItemInline]   # товари показуємо як inline


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('plant', 'user_name', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user_name', 'plant__name')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)