from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
    def get_by_natural_key(self, username):
        # Busca al usuario utilizando el campo definido en USERNAME_FIELD
        return self.get(**{self.model.USERNAME_FIELD: username})

    def create_user(self, nombre_usuario, password=None, nombre=None, apellido=None, email=None, telefono=None, fecha_nacimiento=None, genero=None, rol='usuario'):
        if not nombre_usuario:
            raise ValueError('El usuario debe tener un nombre de usuario')
        user = self.model(
            nombre_usuario=nombre_usuario,
            nombre=nombre,
            apellido=apellido,
            email=self.normalize_email(email),
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            genero=genero,
            rol=rol
        )
        
        user.set_password(password)  # Cifra la contraseña
        user.save(using=self._db)
        return user
    
    def create_superuser(self, nombre_usuario, password=None, nombre=None, apellido=None, email=None, telefono=None, fecha_nacimiento=None, genero=None):
        user = self.create_user(
            nombre_usuario=nombre_usuario,
            password=password,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento,
            genero=genero,
            rol='administrador'  # El rol del superusuario será 'administrador'
        )
        user.is_staff = True  # Asegura que el superusuario es staff
        user.is_superuser = True  # Asegura que el superusuario tiene permisos totales
        user.save(using=self._db)  # Guarda el superusuario en la base de datos
        return user