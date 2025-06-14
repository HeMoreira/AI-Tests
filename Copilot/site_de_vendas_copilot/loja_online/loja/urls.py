# loja/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produto/<str:codigo>/', views.detalhe_produto, name='detalhe_produto'),
    path('carrinho/', views.visualizar_carrinho, name='visualizar_carrinho'),
    path('carrinho/adicionar/<str:codigo>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<str:codigo>/', views.remover_carrinho, name='remover_carrinho'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
]
