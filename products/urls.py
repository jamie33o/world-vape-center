from django.urls import path
from .views import ProductDetailView, ReviewsView, CategoryView

urlpatterns = [
    path('', CategoryView.as_view(), name='categories'),
    path('<str:category>/', CategoryView.as_view(), name='category'),
    path('<str:category>/<str:slug>/', ProductDetailView.as_view(), name='product_details'),
    path('post_review/<int:product_id>', ReviewsView.as_view(), name='post_review'),
    path('delete_review/<int:review_id>', ReviewsView.as_view(), name='delete_review'),
    path('<str:category>', CategoryView.as_view(), name='filter'),
]
