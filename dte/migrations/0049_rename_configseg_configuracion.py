# Generated by Django 5.0.3 on 2024-03-30 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0048_rename_clave_correo_configseg_clavecorreo_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ConfigSeg',
            new_name='Configuracion',
        ),
    ]
