
from django.urls import path
from . import api_views

urlpatterns = [
    path('products/', api_views.ProductListAPI.as_view(), name='api_product_list'),
    path('products/<slug:slug>/', api_views.ProductDetailAPI.as_view(), name='api_product_detail'),
    path('categories/', api_views.CategoryListAPI.as_view(), name='api_category_list'),
]
