# Generated by Django 5.1.5 on 2025-01-26 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_remove_usuario_contrasenia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planta',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
