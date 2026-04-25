from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    nombres = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'controls', 'placeholder': 'Nombres'}))
    apellidos = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'controls', 'placeholder': 'Apellidos'}))
    tipo_documento = forms.ChoiceField(
        choices=Usuario._meta.get_field('tipo_documento').choices,
        widget=forms.Select(attrs={'class': 'controls'})
    )
    numero_documento = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'controls', 'placeholder': 'Número de documento'}))
    direccion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'controls', 'placeholder': 'Dirección'}))
    ciudad = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'controls', 'placeholder': 'Ciudad'}))
    telefono = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'controls', 'placeholder': 'Teléfono'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'controls', 'placeholder': 'Correo electrónico'}))
    
    # Sobrescribir los campos de contraseña para agregar clases CSS
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'controls', 'placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'controls', 'placeholder': 'Confirmar contraseña'}),
    )

    class Meta:
        model = Usuario
        fields = ['email', 'nombres', 'apellidos', 'tipo_documento', 'numero_documento', 
            'direccion', 'ciudad', 'telefono', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # El username se genera automáticamente en el modelo
        if commit:
            user.save()
        return user


class LoginUsuarioForm(AuthenticationForm):
    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'controls', 'placeholder': 'Correo electrónico', 'autofocus': True})
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'controls', 'placeholder': 'Contraseña'}),
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'password']