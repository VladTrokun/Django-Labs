from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Plant(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='plants', verbose_name="Категорія")
    name = models.CharField(max_length=200, verbose_name="Назва рослини")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    is_available = models.BooleanField(default=True, verbose_name="В наявності")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рослина"
        verbose_name_plural = "Рослини"

class ServiceRequest(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Ім'я клієнта")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Повідомлення/Запит")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата запиту")

    def __str__(self):
        return f"Запит від {self.customer_name}"

    class Meta:
        verbose_name = "Запит на послугу"
        verbose_name_plural = "Запити на послуги"