from django.urls import path
from .views import lista_posts

urlpatterns = [
    path('posts/', lista_posts, name='lista_posts'),
]