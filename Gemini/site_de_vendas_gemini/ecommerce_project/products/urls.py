# products/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('categoria/<slug:category_slug>/', views.product_list_view, name='product_list_by_category'),
    path('<slug:slug>/', views.product_detail_view, name='product_detail'),
]