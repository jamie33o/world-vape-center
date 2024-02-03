from django.urls import path
from .views import ProductDetailView, ReviewsView, CategoryView

urlpatterns = [
    path('', CategoryView.as_view(), name='categories'),
    path('category/<str:category>/', CategoryView.as_view(), name='category'),
    path('product_details/<str:slug>/', ProductDetailView.as_view(), name='product_details'),
    path('post_review/<int:product_id>/', ReviewsView.as_view(), name='post_review'),
    path('delete_review/<int:review_id>/', ReviewsView.as_view(), name='delete_review'),
    path('filter/<str:category>', CategoryView.as_view(), name='filter'),
]
