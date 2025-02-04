
from django.urls import path
from . import views



urlpatterns = [
    path('', views.inicio, name='inicio'),  # Página inicial
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('usuario_home/', views.usuario_home, name='usuario_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('gestion_plantas/', views.gestion_plantas, name='gestion_plantas'),  # Gestión de plantas
    path('perfil_admin/', views.perfil_admin, name='perfil_admin'),  # Perfil del administrador
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),  # Perfil del usuario
    path('actualizar_usuario/', views.actualizar_usuario, name='actualizar_usuario'),  # Nueva entrada para actualizar usuarios
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),  # Entrada para eliminar usuarios
    path('actualizar_planta/<int:planta_id>/', views.actualizar_planta, name='actualizar_planta'),  # 🔹 Aquí se corrige
    path('crear_planta/', views.crear_planta, name='crear_planta'),
    path('eliminar_planta/<int:planta_id>/', views.eliminar_planta, name='eliminar_planta'),
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('plantas_usuario/', views.plantas_usuario, name='plantas_usuario'),
    path('añadir_planta_personalizada/', views.añadir_planta_personalizada, name='añadir_planta_personalizada'),
    path('actualizar_planta_personalizada/', views.actualizar_planta_personalizada, name='actualizar_planta_personalizada'),
    path('usuario/eliminar_planta_personalizada/<int:planta_usuario_id>/', views.eliminar_planta_personalizada, name='eliminar_planta_personalizada'),
    path('seleccionar_planta/', views.vista_seleccionar_planta, name='seleccionar_planta'),

]

