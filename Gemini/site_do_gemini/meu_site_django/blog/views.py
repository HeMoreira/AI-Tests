# blog/views.py
from django.shortcuts import render
from .models import Post # Importe seu modelo Post

def lista_posts(request):
    # Busca todos os objetos Post do banco de dados e os ordena pela data de publicação (mais recentes primeiro)
    posts = Post.objects.all().order_by('-data_publicacao')
    # Cria um dicionário de contexto para passar os posts para o template
    context = {
        'posts': posts
    }
    # Renderiza o template 'blog/lista_posts.html', passando o contexto
    return render(request, 'blog/lista_posts.html', context)