from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['nome', 'email', 'conteudo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu email'
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escreva seu comentário...'
            })
        }
        labels = {
            'nome': 'Nome',
            'email': 'Email',
            'conteudo': 'Comentário'
        }