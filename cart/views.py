from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect,render
from django.views.decorators.http import require_POST
from shop.models import Product

from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))  # Получаем количество из запроса
        override = request.POST.get('override_quantity') == 'True'
    except ValueError:
        quantity = 1
    
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=override)
    else:
        cart.remove(product)  # Если количество равно 0, удаляем товар из корзины
    
    # Если запрос через AJAX, возвращаем обновленные данные
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': len(cart),
            'cart_total_price': str(cart.get_total_price())
        })
    
    return redirect('cart:cart_detail')
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )
    return render(request, 'cart/detail.html', {'cart': cart})

def clear_cart_if_session_expired(request):
    if not request.session.exists(request.session.session_key):
        cart = Cart(request)
        cart.clear()
