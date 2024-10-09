from django.conf import settings
from .cart import Cart

class CartSessionMiddleware:
    """
    Middleware to clear the cart when the session expires or the browser is closed.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the session exists, and if not or expired, clear the cart
        if not request.session.session_key or not request.session.exists(request.session.session_key):
            cart = Cart(request)
            cart.clear()

        # Proceed with the response
        response = self.get_response(request)
        return response
