from django import template

register = template.Library()

@register.filter
def get_item(cart, product_id):
    """
    Template filter to get the quantity of an item in the cart.
    """
    return cart.get(str(product_id), {}).get('quantity', 0)
