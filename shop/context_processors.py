from .models import Category


def categories(request):
    return {'categories': Category.objects.all()}


def cart_total_qty(request):
    cart = request.session.get('cart', {})
    total = sum(cart.values())
    return {'cart_total_qty': total}