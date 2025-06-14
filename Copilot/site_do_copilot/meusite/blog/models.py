from django.db import models
from django.utils import timezone

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo  # Representação do objeto no admin