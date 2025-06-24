from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilCliente, Produto, Categoria

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            PerfilCliente.objects.create(user=user)
        return user

class FiltrosProdutoForm(forms.Form):
    nome = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nome do produto'}))
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False, empty_label="Todas as categorias")
    preco_min = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Preço mínimo'}))
    preco_max = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Preço máximo'}))
    
    ORDENACAO_CHOICES = [
        ('prioridade', 'Prioridade'),
        ('-data_cadastro', 'Mais recentes'),
        ('data_cadastro', 'Mais antigos'),
        ('preco', 'Menor preço'),
        ('-preco', 'Maior preço'),
        ('nome', 'Nome A-Z'),
        ('-nome', 'Nome Z-A'),
    ]
    
    ordenacao = forms.ChoiceField(choices=ORDENACAO_CHOICES, required=False)