from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.contrib import messages
from .models import Plant, Category, Review, Newsletter
from .forms import ReviewForm, NewsletterForm


def home(request):
    categories = Category.objects.all()
    plants = Plant.objects.all()
    newsletter_form = NewsletterForm()

    context = {
        'title': 'Vita Garden',
        'description': 'Магазин кімнатних рослин',
        'categories': categories,
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
    categories = Category.objects.all()
    return render(request, 'page1.html', {
        'plants': plants,
        'categories': categories,
    })


def about(request):
    categories = Category.objects.all()
    return render(request, 'page2.html', {
        'info': 'Ми продаємо найкращі рослини 🌿',
        'categories': categories,
    })


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    plants = category.plants.all()
    categories = Category.objects.all()
    return render(request, 'page4.html', {
        'category': category,
        'plants': plants,
        'categories': categories,
    })


def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    categories = Category.objects.all()
    reviews = plant.reviews.all().order_by('-created_at')

    # Середня оцінка + розбивка по зірках для прогрес-барів
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
            review.save()
            messages.success(request, f'Дякуємо за ваш відгук, {review.user_name}! 🌿')
            return redirect('plant_detail', pk=pk)
        else:
            messages.error(request, 'Будь ласка, перевірте правильність заповнення форми.')
    else:
        form = ReviewForm()

    # Цілі зірки для відображення середньої оцінки
    full_stars = int(average_rating)
    has_half = (average_rating - full_stars) >= 0.5
    empty_stars = 5 - full_stars - (1 if has_half else 0)

    return render(request, 'page3.html', {
        'plant': plant,
        'categories': categories,
        'reviews': reviews,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'rating_breakdown': rating_breakdown,
        'full_stars': range(full_stars),
        'has_half': has_half,
        'empty_stars': range(empty_stars),
        'form': form,
    })


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
    categories = Category.objects.all()

    for plant_id, quantity in cart.items():
        plant = get_object_or_404(Plant, id=plant_id)
        subtotal = plant.price * quantity
        total_price += subtotal
        total_qty += quantity
        cart_items.append({'plant': plant, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_qty': total_qty,
        'categories': categories,
    })


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Дякуємо за підписку! 🌱 Скоро надішлемо перший лист.')
        else:
            # Найчастіша помилка — вже існує такий email
            if Newsletter.objects.filter(email=request.POST.get('email', '')).exists():
                messages.info(request, 'Цей email вже підписаний на розсилку 💚')
            else:
                messages.error(request, 'Перевірте коректність email-адреси.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Ваш кошик порожній.')
        return redirect('plants')

    if request.method == 'POST':
        request.session['cart'] = {}
        messages.success(request, 'Замовлення успішно оформлено! 🌿 Ми скоро з вами зв’яжемося.')
        return render(request, 'success.html', {'categories': Category.objects.all()})

    return render(request, 'checkout.html', {'categories': Category.objects.all()})


def top_plants(request):
    plants = Plant.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=4)
    return render(request, 'page1.html', {
        'plants': plants,
        'categories': Category.objects.all(),
        'title': 'Найкращі рослини',
    })


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


def remove_from_cart(request, plant_id):
    cart = request.session.get('cart', {})
    if str(plant_id) in cart:
        plant = Plant.objects.filter(id=plant_id).first()
        del cart[str(plant_id)]
        request.session['cart'] = cart
        if plant:
            messages.info(request, f'«{plant.name}» видалено з кошика.')
    return redirect('cart_detail')
