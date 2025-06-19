# orders/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('finalizar/', views.checkout_view, name='checkout_page'),
    path('confirmacao/<str:order_number>/', views.order_confirmation_view, name='order_confirmation'),
    path('<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('', views.order_list_view, name='order_list'), # Para listar todos os pedidos do cliente
]