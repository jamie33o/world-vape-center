from django.urls import path
from .views import Categories, ProductDetail, Reviews

urlpatterns = [
    path('category/<str:category>/', Categories.as_view(), name='category'),
    path('product_details/<int:product_id>/', ProductDetail.as_view(), name='product_details'),
    path('post_review/<int:product_id>/', Reviews.as_view(), name='post_review'),
]
