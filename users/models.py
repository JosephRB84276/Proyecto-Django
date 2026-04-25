from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    """Manager personalizado para el modelo Usuario"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        
        # Auto-generar username único a partir del email si no se proporciona
        if not extra_fields.get('username'):
            username = email.split('@')[0]
            # Asegurar unicidad agregando números si es necesario
            base_username = username
            counter = 1
            while Usuario.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            extra_fields['username'] = username
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Valores por defecto para campos obligatorios
        extra_fields.setdefault('nombres', 'Admin')
        extra_fields.setdefault('apellidos', 'Sandes')
        extra_fields.setdefault('tipo_documento', 'CC')
        extra_fields.setdefault('numero_documento', '0000000000')
        extra_fields.setdefault('direccion', 'Dirección por defecto')
        extra_fields.setdefault('ciudad', 'Mosquera')
        extra_fields.setdefault('telefono', '3000000000')
        
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    tipo_documento = models.CharField(max_length=20, choices=[
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
        ('NIT', 'NIT')
    ])
    numero_documento = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'tipo_documento', 
        'numero_documento', 'direccion', 'ciudad', 'telefono']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    def get_full_name(self):
        return f"{self.nombres} {self.apellidos}"
    
    def save(self, *args, **kwargs):
        # Auto-generar username si no existe (para usuarios creados fuera del manager)
        if not self.username:
            username = self.email.split('@')[0] if self.email else f"user_{self.id or ''}"
            base_username = username
            counter = 1
            # Evitar conflicto con usernames existentes
            while Usuario.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)