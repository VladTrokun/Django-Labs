from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# --- 1. Категорії ---
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# --- 2. Рослини ---
class Plant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='plants')
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    light = models.CharField(max_length=100, default="Яскраве розсіяне", blank=True)
    watering = models.CharField(max_length=100, default="Помірний", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# --- 3. Замовлення ---
class Order(models.Model):
    # null=True, blank=True дозволить купувати гостям, якщо захочете
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=200, blank=True, default='')
    customer_phone = models.CharField(max_length=20, blank=True, default='')
    customer_email = models.EmailField(blank=True, default='')
    customer_city = models.CharField(max_length=100, blank=True, default='')
    customer_city_ref = models.CharField(max_length=100, blank=True, default='')
    customer_warehouse = models.CharField(max_length=300, blank=True, default='')
    customer_warehouse_ref = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Замовлення #{self.id} - {self.user.username if self.user else 'Гість'}"

# --- 4. Товари в замовленні ---
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    # Додаємо ціну покупки, щоб вона зафіксувалась (якщо ціна рослини зміниться в майбутньому)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.plant.name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity

# --- 5. Відгуки ---
class Review(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100, verbose_name="Ваше ім'я")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оцінка"
    )
    comment = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Оцінка {self.rating} для {self.plant.name}"

# --- 6. Підписка на розсилку ---
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email