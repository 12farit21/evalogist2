from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from .models import Category, Product

from cart.cart import Cart
from cart.forms import CartAddProductForm

from django.db.models import Q

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    query = request.GET.get('q')  # Получаем поисковый запрос
    products = Product.objects.filter(available=True)

    all_item_count = products.count()  # Подсчитываем количество всех товаров
    cart_product_form = CartAddProductForm()

    # Если есть поисковый запрос, фильтруем товары по названию
    if query:
        products = products.filter(Q(name__icontains=query))

    # Если slug категории присутствует, фильтруем товары по этой категории
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        category_items = {
            selected_category.name: list(
                products.filter(category=selected_category, available=True)
            )
        }
    else:
        # Если slug отсутствует, выводим все товары по категориям
        if query:
            # Фильтруем товары в рамках всех категорий по поисковому запросу
            category_items = {
                category.name: list(
                    products.filter(category=category, available=True)
                ) for category in categories if products.filter(category=category).exists()
            }
        else:
            # Если нет поискового запроса, показываем все товары
            category_items = {
                category.name: list(
                    Product.objects.filter(category=category, available=True)
                ) for category in categories
            }
    
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )


# Пагинация по категориям
    paginator = Paginator(categories, 1)  # Пагинация по 3 категории на страницу
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Получаем все товары для отображаемых на странице категорий
    category_items = {
        category.name: list(Product.objects.filter(category=category, available=True)) for category in page_obj
    }

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )

    cart_items = {str(item['product'].id): item['quantity'] for item in cart}  # Собираем информацию о товарах в корзине

    # AJAX запрос для подгрузки следующих категорий
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('shop/product/test.html', {'category_items': category_items})
        return JsonResponse({'html': html, 'cart_items': cart_items, 'has_next': page_obj.has_next()})

    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'category_items': category_items,  # Пагинированные категории и их товары
            'all_item_count': all_item_count,
            'categories': page_obj,  # Пагинация категорий
            'categories_objects':categories,
            'cart_product_form': cart_product_form,
            'cart': cart,
            'products': products,
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product, 
            'cart_product_form': cart_product_form,
            
        },
    )


from django.views import View

class TwitterView(View):

    def get(self, request, forum, *args, **kwargs):
        # Template to render
        template_name = "shop/product/list.html"
        page_template = "shop/product/test.html"

        # Fetch all products
        products = Product.objects.all()

        # Context data
        data = {
            'products': products,
        }

        # Check for AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            template_name = page_template

        # Render the template with context
        return render(request, template_name, data)
    
def category_products(request, category_slug):
    # Get the selected category
    category = get_object_or_404(Category, slug=category_slug)
    
    # Filter products by the selected category
    products = Product.objects.filter(category=category, available=True)
    
    # Initialize the form for adding to cart
    cart_product_form = CartAddProductForm()
    
    # Render the page
    return render(
        request, 
        'shop/product/category_list.html', 
        {
            'category': category, 
            'products': products,
            'cart_product_form': cart_product_form,
        }
    )

def search_products(request):
    query = request.GET.get('q', '')  # Get search query
    products = Product.objects.filter(available=True)  # Get available products

    if query:
        # Filter products by name based on query
        products = products.filter(Q(name__icontains=query))

    # Organize products by category
    categories = Category.objects.all()
    category_items = {
        category.name: list(
            products.filter(category=category, available=True)
        ) for category in categories if products.filter(category=category).exists()
    }

    all_item_count = products.count()  # Count all matching products
    cart_product_form = CartAddProductForm()

    return render(
        request,
        'shop/product/search_results.html',  # New template to display search results
        {
            'category_items': category_items,  # Products grouped by category
            'query': query,  # To display search query
            'all_item_count': all_item_count,  # To show the total number of products found
            'cart_product_form': cart_product_form,
        },
    )