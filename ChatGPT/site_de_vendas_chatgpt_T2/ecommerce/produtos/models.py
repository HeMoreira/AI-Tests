from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    categoria_pai = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategorias')

    def __str__(self):
        return self.nome

class Produto(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    descricao_curta = models.CharField(max_length=200)
    prioridade = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.nome
