# blog/urls.py
from django.urls import path
from . import views # Importe suas views do app 'blog'

app_name = 'blog' # Define um namespace para as URLs do app

urlpatterns = [
    path('', views.lista_posts, name='lista_posts'), # URL para a lista de posts
]