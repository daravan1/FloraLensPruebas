from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UsuarioManager  # Importa el manager personalizado
from django.contrib.auth.models import PermissionsMixin

# Crear tus modelos aquí.
# Aquí se crean las clases que representan las tablas de la base de datos

roles = (
        ('usuario', 'Usuario'), # Opción para usuario
        ('administrador', 'Administrador'), # Opción para administrador
    )

GENERO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro'),
    ('N', 'Prefiero no decirlo'),
]

class Usuario(AbstractBaseUser, PermissionsMixin): 
    nombre = models.CharField(max_length=50) # Campo de texto para el nombre
    apellido = models.CharField(max_length=50) # Campo de texto para el apellido
    nombre_usuario = models.CharField(max_length=150, unique=True)  # Nuevo campo    
    email = models.EmailField() # Campo de texto para el email
    telefono = models.IntegerField() # Campo de texto para el teléfono
    fecha_nacimiento = models.DateField() # Campo de fecha para la fecha de nacimiento
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)  # Campo de texto para el género
    
    rol = models.CharField(max_length=13, choices=roles, default='usuario') # Campo de texto para el rol
    
    is_active = models.BooleanField(default=True)  # Campo obligatorio
    is_staff = models.BooleanField(default=False)  # Necesario para acceder al panel de admin
    is_superuser = models.BooleanField(default=False)  # Para usuarios con permisos totales


    USERNAME_FIELD = 'nombre_usuario'  # Campo de texto para el nombre de usuario
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'genero']  
    # Lista de campos adicionales obligatorios
    objects = UsuarioManager()

    def __str__(self):
        return self.nombre + ' ' + self.apellido # retorna el nombre del usuario porque es un campo obligatorio

class Planta(models.Model): # Clase para la tabla de plantas
    nombre_comun = models.CharField(max_length=50) # Campo de texto para el nombre de la palnta
    nombre_cientifico = models.CharField(max_length=50) # Campo de texto para el nombre científico
    especie = models.CharField(max_length=50) # Campo de texto para la especie
    descripcion = models.TextField() # Campo de texto para la descripción
# Llenar la carpeta de imagenes
    imagen = models.ImageField(upload_to='static/imagenesPlanta') # Campo de imagen para la foto de la planta  
    fecha_registro = models.DateTimeField(auto_now_add=True) # Campo de fecha para la fecha de siembra
    estado_conservacion = models.CharField(max_length=50) # Campo de texto para el estado de conservación
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE) # usuario que registro planta
# tags = models.ManyToManyField(Tag) # Relación muchos a muchos con la tabla de tags
    def __str__(self):
        return self.nombre_comun + ' ' + self.especie # Retorna el nombre de la planta 


class Categoria(models.Model): # Clase para la tabla de plantas
    nombre_categoria = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Planta_Categoria(models.Model):
    planta = models.ForeignKey(
        Planta, on_delete=models.CASCADE, related_name='planta_categorias'
    )  # Relación con Planta
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name='categoria_plantas'
    )  # Relación con Categoria

    def __str__(self):
        return f"{self.planta.nombre_comun} - {self.categoria.nombre_categoria}"
    
class Plantas_Usuario(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE) # Relación uno a muchos con la tabla de plantas
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE) # Relación uno a muchos con la tabla de usuarios
    lugar = models.CharField(max_length=255)
    descripcion_personalizada = models.TextField()

    class Meta:
        unique_together = ('planta', 'usuario')

    def __str__(self):
        return self.planta.nombre + ' ' + self.usuario.nombre
    