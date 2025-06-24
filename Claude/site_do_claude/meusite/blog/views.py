from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Post, Categoria, Comentario
from .forms import ComentarioForm

def home(request):
    """Página inicial com posts recentes"""
    posts_recentes = Post.objects.filter(status='publicado').order_by('-publicado_em')[:6]
    categorias = Categoria.objects.all()
    
    context = {
        'posts_recentes': posts_recentes,
        'categorias': categorias,
        'titulo_pagina': 'Blog - Página Inicial'
    }
    return render(request, 'blog/home.html', context)

def lista_posts(request):
    """Lista todos os posts com filtros e busca"""
    posts = Post.objects.filter(status='publicado').order_by('-publicado_em')
    categorias = Categoria.objects.all()
    
    # Filtro por categoria
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posts = posts.filter(categoria_id=categoria_id)
    
    # Busca por texto
    busca = request.GET.get('busca')
    if busca:
        posts = posts.filter(
            Q(titulo__icontains=busca) | 
            Q(conteudo__icontains=busca) |
            Q(resumo__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(posts, 6)  # 6 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'categoria_selecionada': categoria_id,
        'busca': busca,
        'titulo_pagina': 'Todos os Posts'
    }
    return render(request, 'blog/lista_posts.html', context)

def detalhe_post(request, slug):
    """Página de detalhe do post com comentários"""
    post = get_object_or_404(Post, slug=slug, status='publicado')
    
    # Incrementar visualizações
    post.visualizacoes += 1
    post.save()
    
    # Comentários
    comentarios = post.comentarios.filter(ativo=True).order_by('criado_em')
    
    # Formulário de comentário
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.save()
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('blog:detalhe_post', slug=slug)
    else:
        form = ComentarioForm()
    
    # Posts relacionados (mesma categoria)
    posts_relacionados = Post.objects.filter(
        categoria=post.categoria, 
        status='publicado'
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'posts_relacionados': posts_relacionados,
        'titulo_pagina': post.titulo
    }
    return render(request, 'blog/detalhe_post.html', context)

def posts_por_categoria(request, categoria_id):
    """Posts filtrados por categoria"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(categoria=categoria, status='publicado').order_by('-publicado_em')
    
    # Paginação
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categoria': categoria,
        'titulo_pagina': f'Posts em {categoria.nome}'
    }
    return render(request, 'blog/posts_categoria.html', context)

def curtir_post(request, post_id):
    """AJAX para curtir post"""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        # Aqui você pode implementar um sistema de curtidas mais complexo
        # Por enquanto, vamos apenas incrementar as visualizações como proxy
        post.visualizacoes += 1
        post.save()
        
        return JsonResponse({
            'success': True,
            'curtidas': post.visualizacoes
        })
    
    return JsonResponse({'success': False})