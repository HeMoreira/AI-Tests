# customers/models.py

from django.db import models
from django.contrib.auth.models import User # Importa o modelo de usuário padrão do Django

class CustomerProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Usuário")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="Gênero")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone")
    address = models.TextField(null=True, blank=True, verbose_name="Endereço")
    zip_code = models.CharField(max_length=10, null=True, blank=True, verbose_name="CEP")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=100, null=True, blank=True, verbose_name="Estado")
    country = models.CharField(default='Brasil', max_length=100, verbose_name="País")

    class Meta:
        verbose_name = "Perfil do Cliente"
        verbose_name_plural = "Perfis dos Clientes"

    def __str__(self):
        return self.user.username