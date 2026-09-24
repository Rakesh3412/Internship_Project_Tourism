from .models import State, Category

def global_tourism_context(request):
    """
    Context processor to inject states, categories, and wishlist items count globally
    """
    states = State.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    
    # Wishlist from session
    wishlist = request.session.get('wishlist', [])
    
    return {
        'nav_states': states,
        'nav_categories': categories,
        'wishlist_items_count': len(wishlist),
    }
