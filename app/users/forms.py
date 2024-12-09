from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'role', 'empresa','password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese su email',
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese su contraseña',
        })
    )
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'empresa', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': _('El nombre de usuario es obligatorio.'),
            },
            'email': {
                'invalid': _('Introduce un correo electrónico válido.'),
                'required': _('El correo electrónico es obligatorio.'),
            },
            'password2': {
                'required': _('Por favor, confirma tu contraseña.'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control w-50'
            # field.widget.attrs['placeholder'] = field.label  # Añade el label como placeholder
            field.label = field.label.capitalize()  # Capitaliza los labels
            for field_name, field in self.fields.items():
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select w-50'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está en uso.")
        return email
    
class AutoRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'empresa', 'password1', 'password2']  # Excluye el campo 'role'
        error_messages = {
            'username': {
                'required': _('El nombre de usuario es obligatorio.'),
            },
            'email': {
                'invalid': _('Introduce un correo electrónico válido.'),
                'required': _('El correo electrónico es obligatorio.'),
            },
            'password2': {
                'required': _('Por favor, confirma tu contraseña.'),
            },
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'
            # field.widget.attrs['placeholder'] = field.label  # Añade el label como placeholder
            field.label = field.label.capitalize()  # Capitaliza los labels

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'CLIENT'  # Asignar el rol predeterminado
        if commit:
            user.save()
        return user
    

class CustomUserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput,
        required=False,
        help_text="Dejar en blanco si no desea cambiar la contraseña."
    )
    password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput,
        required=False,
        help_text="Ingrese la misma contraseña para confirmación."
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'empresa']  # Los campos adicionales están aquí
        error_messages = {
            'username': {
                'required': _('El nombre de usuario es obligatorio.'),
            },
            'email': {
                'invalid': _('Introduce un correo electrónico válido.'),
                'required': _('El correo electrónico es obligatorio.'),
            },
            'password2': {
                'required': _('Por favor, confirma tu contraseña.'),
            },
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].disabled = True  # Deshabilitar el campo 'email'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control w-50'
            field.label = field.label.capitalize()  # Capitaliza los labels
            for field_name, field in self.fields.items():
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select w-50'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:  # Validar solo si se llenan los campos
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:  # Si se ingresó una nueva contraseña, se actualiza
            user.set_password(password1)
        if commit:
            user.save()
        return user