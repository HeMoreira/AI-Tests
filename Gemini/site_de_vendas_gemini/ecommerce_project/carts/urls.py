# carts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail_view, name='cart_detail'),
    path('adicionar/<str:sku>/', views.add_to_cart, name='add_to_cart'),
    path('remover/<str:sku>/', views.remove_from_cart, name='remove_from_cart'),
    path('atualizar/<str:sku>/', views.update_cart_quantity, name='update_cart_quantity'),
]