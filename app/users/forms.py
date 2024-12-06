from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',  # Clase de Bootstrap u otra clase CSS
            'placeholder': 'Ingrese su email',  # Placeholder personalizado
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',  # Clase de Bootstrap u otra clase CSS
            'placeholder': 'Ingrese su password',  # Placeholder personalizado
        })
    )
