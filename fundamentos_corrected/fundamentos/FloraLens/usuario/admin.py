from django.contrib import admin
from .models import Usuario, Planta

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin): # Clase para mostrar los campos de la tabla de usuarios
    list_display = (
        'id', 
        'nombre', 
        'apellido', 
        'email', 
        'telefono', 
        'fecha_nacimiento', 
        'genero') # Campos que se mostrarán en la tabla de usuarios
    list_filter = (
        'nombre',
        'apellido', 
        'email', 
        'telefono', 
        'fecha_nacimiento', 
        'genero') #  filtrar
    search_fields = (
        'nombre', 
        'apellido', 
        'email', 
        'telefono', 
        'fecha_nacimiento', 
        'genero') # duscar
    ordering = ('id',)

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_comun',
        'nombre_cientifico',
        'especie',
        'descripcion',
        'imagen',
        'fecha_registro',
        'estado_conservacion',
        'usuario_id'
    )
    list_filter = (
        'nombre_comun',
        'nombre_cientifico',
        'especie',
        'descripcion',
        'imagen',
        'fecha_registro',
        'estado_conservacion',
        'usuario_id'
    )
    search_fields = (
        'nombre_comun',
        'nombre_cientifico',
        'especie',
        'descripcion',
        'imagen',
        'fecha_registro',
        'estado_conservacion',
        'usuario_id'
    )
    ordering = ('id',)