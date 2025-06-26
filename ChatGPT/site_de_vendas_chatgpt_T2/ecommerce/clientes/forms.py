from django import forms
from django.contrib.auth.models import User
from .models import Cliente
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['identificador', 'genero', 'data_nascimento']
