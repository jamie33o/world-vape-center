"""
URL patterns for the products app.

This module defines the URL patterns for navigating through the products app.
It includes patterns for searching, viewing categories, product details, posting
and deleting reviews, filtering, and adding to favorites.

URL Patterns:
- search: Handles product search queries.
- categories: Displays all available categories.
- category: Displays products within a specific category.
- product_details: Displays detailed information about a specific product.
- post_review: Handles posting a new review for a product.
- delete_review: Handles deleting a review for a product.
- filter: Handles category-based filtering.
- add_to_favorites: Handles adding a product to the user's favorites.
"""
from django.urls import path
from .views import ProductDetailView, ReviewsView, CategoryView, search, add_to_favorites

urlpatterns = [
    path('search', search, name='search'),
    path('', CategoryView.as_view(), name='categories'),
    path('<str:category>/', CategoryView.as_view(), name='category'),
    path('<str:category>/<str:slug>/', ProductDetailView.as_view(), name='product_details'),
    path('post_review/<int:product_id>', ReviewsView.as_view(), name='post_review'),
    path('delete_review/<int:review_id>', ReviewsView.as_view(), name='delete_review'),
    path('<str:category>', CategoryView.as_view(), name='filter'),
    path('add_to_favorites/<int:product_id>', add_to_favorites, name='add_to_favorites'),
]
