from django.urls import path
from . import views

urlpatterns = [
    path('<str:produto_id>/', views.detalhes_produto, name='detalhes_produto'),
]
