from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})