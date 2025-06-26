from django.http import HttpResponse
from .models import Post

def listar_posts(request):
    posts = Post.objects.all()
    saida = "<h1>Lista de Posts</h1>"
    for post in posts:
        saida += f"<h2>{post.titulo}</h2><p>{post.conteudo}</p><hr>"
    return HttpResponse(saida)