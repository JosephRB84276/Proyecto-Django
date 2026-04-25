from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['email', 'nombres', 'apellidos', 'numero_documento', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal', {'fields': ('nombres', 'apellidos', 'tipo_documento', 
            'numero_documento', 'direccion', 'ciudad', 'telefono')}),
    )