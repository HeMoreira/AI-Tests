from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produto/<str:codigo>/', views.detalhe_produto, name='detalhe_produto'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar-carrinho/<str:codigo>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('remover-carrinho/<str:codigo>/', views.remover_carrinho, name='remover_carrinho'),
    path('atualizar-quantidade/<str:codigo>/', views.atualizar_quantidade, name='atualizar_quantidade'),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
]