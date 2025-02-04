# Generated by Django 5.1.5 on 2025-01-25 21:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('nombre_usuario', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('contrasenia', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=10)),
                ('fecha_nacimiento', models.DateField()),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro'), ('N', 'Prefiero no decirlo')], max_length=1)),
                ('rol', models.CharField(choices=[('usuario', 'Usuario'), ('administrador', 'Administrador')], default='usuario', max_length=13)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_categoria', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_comun', models.CharField(max_length=50)),
                ('nombre_cientifico', models.CharField(max_length=50)),
                ('especie', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(upload_to='static/imagenesPlanta')),
                ('fecha_registro', models.DateField()),
                ('estado_conservacion', models.CharField(max_length=50)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Planta_Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.categoria')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.planta')),
            ],
        ),
        migrations.CreateModel(
            name='Plantas_Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.planta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
