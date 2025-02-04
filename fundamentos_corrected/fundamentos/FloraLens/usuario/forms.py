
from django import forms
from .models import Planta,Usuario
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña", required=True)

    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'nombre_usuario', 'email', 'telefono', 'fecha_nacimiento', 'genero')

    def save(self, commit=True): # Guarda el usuario en la base de datos
        user = super().save(commit=False)
        # Cifra la contraseña y asigna al campo `password`
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    


class PlantaModelForm (forms.ModelForm): # Formulario para añadir plantas
    class Meta: # Clase para definir los campos del formulario
        model = Planta
        fields = ['nombre_comun', 'nombre_cientifico', 'especie', 'descripcion', 'imagen', 'estado_conservacion']

class PlantaForm(forms.Form): # Formulario para añadir plantas personalizadas
    planta_id = forms.ModelChoiceField( # Campo de selección de plantas
        queryset=Planta.objects.all(),
        label="Planta", # Etiqueta del campo
        widget=forms.Select(attrs={'class': 'form-control'}) # Atributos del campo
    )
    lugar = forms.CharField( # Campo de texto para el lugar
        max_length=255,
        label="Lugar",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    descripcion_personalizada = forms.CharField(
        label="Descripción personalizada",
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False
    )


class añadir_planta_personalizada_forms(forms.Form):
    planta_id = forms.ModelChoiceField(
        queryset=Planta.objects.all(),  # Esto se sobrescribe en la vista
        label="Selecciona una planta",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    lugar = forms.CharField(
        max_length=255,
        label="Lugar",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    descripcion_personalizada = forms.CharField(
        label="Descripción personalizada",
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False,
    )