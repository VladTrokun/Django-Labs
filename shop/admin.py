from django.contrib import admin
from .models import Category, Plant, ServiceRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    # Відображаємо назву, ціну, наявність та дати
    list_display = ('name', 'category', 'price', 'is_available', 'created_at', 'updated_at')
    # Додаємо фільтрацію справа
    list_filter = ('is_available', 'category', 'created_at')
    # Можливість пошуку за назвою
    search_fields = ('name',)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'email', 'created_at')
    readonly_fields = ('created_at',) # Робимо дату тільки для читання