from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produto/<int:id>/', views.info_produto, name='info_produto'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover/<int:item_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('atualizar/<int:item_id>/', views.atualizar_quantidade, name='atualizar_quantidade'),
    path('finalizar-pedido/', views.finalizar_pedido, name='finalizar_pedido'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),

]