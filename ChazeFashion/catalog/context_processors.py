
def catalog_context(request):
    """
    Example context processor. You can add common data here that you want
    available in all templates.
    """
    # Example: You might want to pass the current user's cart item count
    # or a list of main categories to all templates.
    # from .models import CartItem, Product # Uncomment if needed
    #
    # cart_item_count = 0
    # if request.user.is_authenticated:
    #     try:
    #         cart = request.user.cart
    #         cart_item_count = cart.items.count()
    #     except AttributeError:
    #         # User might not have a cart yet, or cart field is not directly on User
    #         pass

    return {
        # 'cart_item_count': cart_item_count, # Example of data you might add
        'app_name': 'ChazeFashion', # Example of a global variable
    }

