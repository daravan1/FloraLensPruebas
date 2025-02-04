
from django.contrib import admin
from django.urls import path, include
from usuario import views
from django.shortcuts import redirect
from usuario.views import inicio
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('usuario/', include('usuario.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
