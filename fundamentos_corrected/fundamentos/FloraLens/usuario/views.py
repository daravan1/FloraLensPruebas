from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Planta, Plantas_Usuario, Categoria, Planta_Categoria
from .forms import PlantaForm, LoginForm, UserRegistrationForm, añadir_planta_personalizada_forms, PlantaModelForm
from django.contrib import messages
from django.urls import reverse
from django.db.models import Prefetch
import json




User = get_user_model()  # Obtén el modelo de usuario personalizado


#Vista de página de inicio
def inicio(request):
    return render(request, 'inicio.html', {'section': 'inicio'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Verifica el rol del usuario y redirige según corresponda
                    if hasattr(user, 'rol'):  # Verifica si el usuario tiene el atributo `rol`
                        if user.rol == 'administrador':
                            return redirect(reverse('admin_home'))  # Redirige al home de administrador
                        elif user.rol == 'usuario':
                            return redirect(reverse('usuario_home'))  # Redirige al home de usuario
                        else:
                            # Si el rol no es válido, muestra un error
                            return render(request, 'registro/login.html', {'form': form, 'error': 'Rol desconocido.'})
                    else:
                        # Si el usuario no tiene un atributo `rol`, muestra un error
                        return render(request, 'registro/login.html', {'form': form, 'error': 'El usuario no tiene un rol asignado.'})
                else:
                    return render(request, 'registro/login.html', {'form': form, 'error': 'Cuenta no activa.'})
            else:
                return render(request, 'registro/login.html', {'form': form, 'error': 'Credenciales incorrectas.'})
    else:
        form = LoginForm()
    return render(request, 'registro/login.html', {'form': form})

def usuario_home(request):
    # Prefetch relacionado para obtener las categorías asociadas a las plantas
    categorias_prefetch = Prefetch(
        'planta_categorias',  # Nombre del related_name en Planta_Categoria (ajústalo si usas uno diferente)
        queryset=Planta_Categoria.objects.select_related('categoria')
    )

    # Obtener las plantas personalizadas del usuario autenticado, incluyendo sus categorías
    plantas_personalizadas = Plantas_Usuario.objects.filter(usuario=request.user).select_related(
        'planta'  # Trae la relación con Planta
    ).prefetch_related(
        Prefetch('planta__planta_categorias', queryset=Planta_Categoria.objects.select_related('categoria'))
    )

    plantas_disponibles = Planta.objects.exclude(id__in=plantas_personalizadas.values_list('planta_id', flat=True))
    


    if request.method == 'POST':  # Si la solicitud es POST
        form = PlantaForm(request.POST)
        if form.is_valid():
            planta_id = form.cleaned_data.get('planta_id')  # Suponiendo que el formulario tiene un campo planta_id
            lugar = form.cleaned_data.get('lugar')  # Campo para personalizar el lugar
            descripcion_personalizada = form.cleaned_data.get('descripcion_personalizada')  # Descripción personalizada

            # Verificar si ya existe una personalización para esa planta y usuario
            planta = get_object_or_404(Planta, id=planta_id)
            personalizacion, created = Plantas_Usuario.objects.get_or_create(
                planta=planta,
                usuario=request.user,
                defaults={
                    'lugar': lugar,
                    'descripcion_personalizada': descripcion_personalizada
                }
            )

            if not created:  # Si ya existía, actualiza la personalización
                personalizacion.lugar = lugar
                personalizacion.descripcion_personalizada = descripcion_personalizada
                personalizacion.save()

            return redirect('usuario_home')  # Redirige a la misma vista
    else:
        form = PlantaForm()  # Formulario vacío para solicitudes GET

    # Renderiza la plantilla con las plantas personalizadas y el formulario
    context = {
        'plantas_personalizadas': plantas_personalizadas,
        'plantas_disponibles': plantas_disponibles,
        'form': form,
    }
    return render(request, 'usuario/usuario_home.html', context)

@login_required
def admin_home(request):
    users = User.objects.all()  # Obtiene todos los usuarios de la base de datos
    return render(request, 'admin/admin_home.html', {'users': users})

def signup(request):  # Vista para el registro de usuarios
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.success(request, '¡Tu cuenta se creó exitosamente! Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            print(form.errors)  # Esto mostrará los errores específicos del formulario
            messages.error(request, 'Por favor corrige los errores en el formulario.')

    else:
        form = UserRegistrationForm()
    return render(request, 'registro/signup.html', {'form': form})

@login_required
def gestion_plantas(request):
    plantas = Planta.objects.all() # Obtiene todas las plantas de la base de datos
    
    
    return render(request, 'admin/gestion_plantas.html', {'plantas': plantas})

@login_required
def perfil_admin(request):
    
    return render(request, 'admin/perfil_admin.html')


@login_required
def perfil_usuario(request):
    usuario = request.user
    return render(request, 'usuario/perfil_usuario.html', {'usuario': usuario})

# Actualizar perfil de usuario
def actualizar_usuario(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        usuario = get_object_or_404(User, id=user_id) 
        
        # Obtener y actualizar los datos del formulario
        usuario.nombre = request.POST.get('nombre', usuario.nombre)
        usuario.apellido = request.POST.get('apellido', usuario.apellido)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.telefono = request.POST.get('telefono', usuario.telefono)
        usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento', usuario.fecha_nacimiento)
        usuario.genero = request.POST.get('genero', usuario.genero)

        if request.user.is_superuser:
            usuario.rol = request.POST.get('rol', usuario.rol)

        # Validar y actualizar el nombre de usuario si existe
        nombre_usuario = request.POST.get('nombre_usuario')
        if nombre_usuario:
            usuario.nombre_usuario = nombre_usuario
        
        # Actualizar contraseña si se envió
        password = request.POST.get('password')
        if password:
            usuario.set_password(password)  # Usar set_password para cifrar la contraseña
        
        usuario.save()  # Guardar cambios en la base de datos
        messages.success(request, 'Usuario actualizado correctamente.')

        
        return redirect('login')  # Usuario normal redirige a su perfil
        
    else:
        messages.error(request, 'Solicitud inválida.')
        return redirect('perfil_usuario')  # Redirige al perfil del usuario
    
@login_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('admin_home')

@login_required
def actualizar_planta(request, planta_id):
    print(f"Recibida solicitud para actualizar la planta con ID: {planta_id}")
    planta = get_object_or_404(Planta, id=planta_id)
    
    if request.method == 'POST':
        # Actualiza solo los campos que están en el formulario
        planta.nombre_comun = request.POST.get('nombre_comun', planta.nombre_comun)
        planta.nombre_cientifico = request.POST.get('nombre_cientifico', planta.nombre_cientifico)
        planta.especie = request.POST.get('especie', planta.especie)
        planta.descripcion = request.POST.get('descripcion', planta.descripcion)
        planta.estado_conservacion = request.POST.get('estado_conservacion', planta.estado_conservacion)

        # Si se sube una nueva imagen, se actualiza
        if 'imagen' in request.FILES:
            planta.imagen = request.FILES['imagen']

        try:
            planta.save()
            messages.success(request, 'Planta actualizada correctamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar la planta: {str(e)}')
        
        return redirect('gestion_plantas')

    messages.error(request, 'Método no permitido.')
    return redirect('gestion_plantas')




@login_required
def crear_planta(request):
    if request.method == 'POST':
        form = PlantaModelForm(request.POST, request.FILES)
        if form.is_valid():
            planta = form.save(commit=False)  # Crea el objeto pero no lo guarda aún
            planta.usuario_id = request.user  # Asigna el usuario autenticado
            planta.save()  # Guarda el objeto con el usuario
            messages.success(request, 'La planta fue creada correctamente.')
            print(f"Planta guardada: {planta.nombre_comun}, ID: {planta.id}")  # Depuración

            return redirect('gestion_plantas')  # Redirige después de guardar
        else:
            print(f"Errores en el formulario: {form.errors}")  # Esto mostrará los errores específicos del formulario
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = PlantaForm()
    return render(request, 'admin/gestion_plantas.html', {'form': form})

@login_required
def eliminar_planta(request, planta_id):
    planta = get_object_or_404(Planta, id=planta_id)
    planta.delete()
    messages.success(request, 'La planta fue eliminada correctamente.')
    return redirect('gestion_plantas')

# actualizar perfil de administrador
def actualizar_perfil(request):
    if request.method == 'POST':
        usuario = request.user  # Usuario autenticado
        
        # Obtener y actualizar los datos del formulario
        usuario.nombre = request.POST.get('nombre')
        usuario.apellido = request.POST.get('apellido')
        usuario.nombre_usuario = request.POST.get('nombre_usuario')
        usuario.email = request.POST.get('email')
        usuario.password = request.POST.get('password')
        usuario.telefono = request.POST.get('telefono')
        usuario.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        usuario.genero = request.POST.get('genero')
        
        # Validar y actualizar el nombre de usuario si existe
        nombre_usuario = request.POST.get('nombre_usuario')
        if nombre_usuario:
            usuario.nombre_usuario = nombre_usuario

        # Actualizar contraseña si se envió
        password = request.POST.get('password')
        if password:
            usuario.set_password(password)  # Usar set_password para cifrar la contraseña

        usuario.save()  # Guardar cambios en la base de datos

        # Mostrar mensaje de éxito y redirigir al perfil de administrador
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('login')  # Nombre del patrón de URL
    else:
        # Manejar solicitudes que no sean POST
        messages.error(request, 'Solicitud inválida.')
        return redirect('perfil_admin')  # Nombre del patrón de URL

@login_required
def perfil_admin(request):
    # Extrae los datos del usuario autenticado
    admin = request.user

    # Pasa los datos al contexto como 'admin' para que coincida con la plantilla
    return render(request, 'admin/perfil_admin.html', {'admin': admin})

def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de inicio de sesión (o donde prefieras)

@login_required
def añadir_planta_personalizada(request):
    
    if request.method == 'POST':
        print(request.POST)

        planta_id = request.POST.get("planta_id")
        lugar = request.POST.get("lugar")
        descripcion = request.POST.get("descripcion_personalizada")

        if planta_id and lugar and descripcion:
            # Lógica para añadir la planta
            planta = get_object_or_404(Planta, id=planta_id)
            nueva_planta  = Plantas_Usuario.objects.create(
                planta=planta,
                usuario=request.user,
                lugar=lugar,
                descripcion_personalizada=descripcion
            )
            nueva_planta.save()
            messages.success(request, "Planta personalizada añadida con éxito.")

            return redirect("usuario_home")  # O la página adecuada
        else:
            messages.error(request, "Faltan datos para añadir la planta.")
            return redirect("usuario_home")
    else:
        return redirect("usuario_home")
    




@login_required
def actualizar_planta_personalizada(request):
    if request.method == 'POST':
        planta_usuario_id = request.POST.get('personalized_plant_id')
        lugar = request.POST.get('lugar')
        descripcion_personalizada = request.POST.get('descripcion_personalizada')

        planta_usuario = get_object_or_404(Plantas_Usuario, id=planta_usuario_id, usuario=request.user)

        # Actualizar los valores
        planta_usuario.lugar = lugar
        planta_usuario.descripcion_personalizada = descripcion_personalizada
        planta_usuario.save()

        messages.success(request, "Planta personalizada actualizada con éxito.")
        return redirect('usuario_home')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('usuario_home')

@login_required
def eliminar_planta_personalizada(request, planta_usuario_id):
    planta_usuario = get_object_or_404(Plantas_Usuario, id=planta_usuario_id, usuario=request.user)

    # Eliminar la planta personalizada
    planta_usuario.delete()

    messages.success(request, "Planta personalizada eliminada con éxito.")
    return redirect('usuario_home')

@login_required
def plantas_usuario(request):
    plantas = Plantas_Usuario.objects.filter(usuario=request.user)
    return render(request, 'usuario/plantas_usuario.html', {'plantas': plantas})



def vista_seleccionar_planta(request):
    plantas_disponibles = Planta.objects.all()  # Cambia el nombre de la variable
    return render(request, 'usuario/seleccionar_planta.html', {'plantas_disponibles': plantas_disponibles})