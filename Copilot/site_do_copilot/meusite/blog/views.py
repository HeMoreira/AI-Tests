from django.shortcuts import render
from .models import Post

def lista_posts(request):
    posts = Post.objects.all()  # Busca todos os posts no banco
    return render(request, 'blog/lista_posts.html', {'posts': posts})