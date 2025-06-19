# blog/admin.py
from django.contrib import admin
from .models import Post # Importe seu modelo Post

admin.site.register(Post) # Registre o modelo