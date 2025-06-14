from django import forms
from django.contrib.auth.models import User
from .models import Cliente

class RegistroUsuarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'identificador', 'genero', 'data_nascimento']
