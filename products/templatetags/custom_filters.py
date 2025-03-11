# custom_filters.py
from django import template
from profile.models import Favourite

register = template.Library()

@register.filter(name='custom_range')
def custom_range(value):
    return range(1, value + 1)


@register.filter(name='is_favorited_by')
def is_favorited_by(product, user):
    """Check if a product is in the user's favorites."""
    if not user.is_authenticated:
        return False
    return Favourite.objects.filter(user=user, products=product).exists()
