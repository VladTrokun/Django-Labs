import os
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.http import require_GET
import requests as http_requests
from .models import Plant, Category, Review, Newsletter, Order, OrderItem
from .forms import ReviewForm, NewsletterForm, RegisterForm
from Myshop.settings import NOVA_POSHTA_API_KEY, NOVA_POSHTA_URL



# --- ГОЛОВНІ СТОРІНКИ ---

def home(request):
    plants = Plant.objects.all()
    newsletter_form = NewsletterForm()

    context = {
        'title': 'Vita Garden',
        'description': 'Магазин кімнатних рослин',
        'plants': plants,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'home.html', context)


def plants(request):
    category_id = request.GET.get('category')
    if category_id:
        plants = Plant.objects.filter(category_id=category_id)
    else:
        plants = Plant.objects.all()
    return render(request, 'catalog.html', {
        'plants': plants,
    })


def about(request):
    return render(request, 'about.html', {
        'info': 'Ми продаємо найкращі рослини 🌿',
    })


# --- ДЕТАЛІ ТА ВІДГУКИ ---

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    plants = category.plants.all()
    return render(request, 'category.html', {
        'category': category,
        'plants': plants,
    })


def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    reviews = plant.reviews.all().order_by('-created_at')

    agg = reviews.aggregate(avg=Avg('rating'), total=Count('id'))
    average_rating = round(agg['avg'] or 0, 1)
    total_reviews = agg['total']

    rating_breakdown = []
    for star in range(5, 0, -1):
        count = reviews.filter(rating=star).count()
        percent = round((count / total_reviews) * 100) if total_reviews else 0
        rating_breakdown.append({'star': star, 'count': count, 'percent': percent})

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.plant = plant
            if request.user.is_authenticated:
                review.user = request.user
            review.save()
            messages.success(request, 'Дякуємо за ваш відгук! 🌿')
            return redirect('plant_detail', pk=pk)
        else:
            messages.error(request, 'Будь ласка, перевірте правильність заповнення форми.')
    else:
        form = ReviewForm()

    full_stars = int(average_rating)
    has_half = False
    empty_stars = 5 - full_stars

    return render(request, 'product.html', {
        'plant': plant,
        'reviews': reviews,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'rating_breakdown': rating_breakdown,
        'full_stars': range(full_stars),
        'has_half': has_half,
        'empty_stars': range(empty_stars),
        'form': form,
    })


# --- КОШИК ---

def add_to_cart(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    cart = request.session.get('cart', {})
    cart[str(plant_id)] = cart.get(str(plant_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f'«{plant.name}» додано в кошик 🛒')
    return redirect(request.META.get('HTTP_REFERER', 'plants'))


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    total_qty = 0

    for plant_id, quantity in cart.items():
        try:
            plant = Plant.objects.get(id=plant_id)
            subtotal = plant.price * quantity
            total_price += subtotal
            total_qty += quantity
            cart_items.append({'plant': plant, 'quantity': quantity, 'subtotal': subtotal})
        except Plant.DoesNotExist:
            continue

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_qty': total_qty,
    })


def remove_from_cart(request, plant_id):
    cart = request.session.get('cart', {})
    if str(plant_id) in cart:
        del cart[str(plant_id)]
        request.session['cart'] = cart
        messages.info(request, 'Товар видалено з кошика.')
    return redirect('cart_detail')


def remove_single_from_cart(request, plant_id):
    cart = request.session.get('cart', {})
    pid = str(plant_id)
    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            del cart[pid]
    request.session['cart'] = cart
    return redirect('cart_detail')


# --- АВТЕНТИФІКАЦІЯ ТА ПРОФІЛЬ ---

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Реєстрація успішна! Тепер ви можете увійти.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {
        'form': form,
    })


@login_required
def profile(request):
    """
    Особистий кабінет:
    - Адмін (is_staff=True) бачить усі замовлення
    - Звичайний користувач бачить лише власні
    """
    if request.user.is_staff:
        orders = Order.objects.all().order_by('-created_at').prefetch_related('items__plant')
    else:
        orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__plant')

    return render(request, 'profile.html', {
        'orders': orders,
    })


@login_required
def order_detail(request, pk):
    if request.user.is_staff:
        order = get_object_or_404(Order, pk=pk)
    else:
        order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'order_detail.html', {'order': order})




def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Ваш кошик порожній.')
        return redirect('plants')

    if request.method == 'POST':
        customer_name = request.POST.get('name', '')
        customer_phone = request.POST.get('phone', '')
        customer_email = request.POST.get('email', '')
        customer_city = request.POST.get('city', '')
        customer_city_ref = request.POST.get('city_ref', '')
        customer_warehouse = request.POST.get('warehouse', '')
        customer_warehouse_ref = request.POST.get('warehouse_ref', '')

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_price=0,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            customer_city=customer_city,
            customer_city_ref=customer_city_ref,
            customer_warehouse=customer_warehouse,
            customer_warehouse_ref=customer_warehouse_ref,
        )

        total = 0
        for plant_id, qty in cart.items():
            plant = get_object_or_404(Plant, id=plant_id)
            subtotal = plant.price * qty
            total += subtotal
            OrderItem.objects.create(order=order, plant=plant, quantity=qty, price=plant.price)

        order.total_price = total
        order.save()

        request.session['cart'] = {}
        messages.success(request, 'Замовлення успішно оформлено! 🌿')
        return render(request, 'success.html')

    return render(request, 'checkout.html', {
        'user_email': request.user.email if request.user.is_authenticated else '',
    })


# --- РОЗСИЛКА ---

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Дякуємо за підписку! 🌱')
        else:
            if Newsletter.objects.filter(email=request.POST.get('email', '')).exists():
                messages.info(request, 'Ви вже підписані 💚')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def top_plants(request):
    plants = Plant.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=4)
    return render(request, 'catalog.html', {
        'plants': plants,
        'title': 'Найкращі рослини',
    })


# --- НОВА ПОШТА API ---

@require_GET
def np_search_cities(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'cities': []})
    try:
        resp = http_requests.post(NOVA_POSHTA_URL, json={
            "apiKey": NOVA_POSHTA_API_KEY,
            "modelName": "Address",
            "calledMethod": "searchSettlements",
            "methodProperties": {
                "CityName": query,
                "Limit": 10,
                "Page": 1,
            }
        }, timeout=5)
        data = resp.json()
        cities = []
        for item in data.get('data', [{}])[0].get('Addresses', []):
            cities.append({
                'ref': item.get('DeliveryCity', ''),
                'name': item.get('Present', ''),
            })
        return JsonResponse({'cities': cities})
    except Exception:
        return JsonResponse({'cities': []})


@require_GET
def np_get_warehouses(request):
    city_ref = request.GET.get('city_ref', '').strip()
    if not city_ref:
        return JsonResponse({'warehouses': []})
    try:
        resp = http_requests.post(NOVA_POSHTA_URL, json={
            "apiKey": NOVA_POSHTA_API_KEY,
            "modelName": "AddressGeneral",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityRef": city_ref,
                "Limit": 100,
                "Page": 1,
            }
        }, timeout=5)
        data = resp.json()
        warehouses = []
        for w in data.get('data', []):
            warehouses.append({
                'ref': w.get('Ref', ''),
                'name': w.get('Description', ''),
            })
        return JsonResponse({'warehouses': warehouses})
    except Exception:
        return JsonResponse({'warehouses': []})