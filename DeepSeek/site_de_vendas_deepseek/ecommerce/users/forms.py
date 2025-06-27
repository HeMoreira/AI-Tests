from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    
    class Meta:
        model = Customer
        fields = ['username', 'email', 'birth_date', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = Customer
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['gender', 'birth_date']