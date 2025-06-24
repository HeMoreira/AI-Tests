from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.lista_posts, name='lista_posts'),
    path('post/<slug:slug>/', views.detalhe_post, name='detalhe_post'),
    path('categoria/<int:categoria_id>/', views.posts_por_categoria, name='posts_por_categoria'),
    path('curtir/<int:post_id>/', views.curtir_post, name='curtir_post'),
]