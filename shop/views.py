from django.shortcuts import render,get_object_or_404
from .models import Plant, Category


def home(request):
    categories = Category.objects.all()

    context = {
        'title': 'Vita Garden',
        'description': 'Магазин кімнатних рослин',
        'categories': categories
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
        'categories': categories
    })


def about(request):
    categories = Category.objects.all()

    return render(request, 'page2.html', {
        'info': 'Ми продаємо найкращі рослини 🌿',
        'categories': categories
    })

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    plants = category.plants.all()
    categories = Category.objects.all()
    return render(request, 'page4.html', {
        'category': category,
        'plants': plants,
        'categories': categories
    })

def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    categories = Category.objects.all()
    return render(request, 'page3.html', {
        'plant': plant,
        'categories': categories
    })