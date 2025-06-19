# blog/models.py
from django.db import models
from django.utils import timezone # Importe timezone para o campo de data

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(default=timezone.now)
    autor = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo