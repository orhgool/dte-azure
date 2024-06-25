# Generated by Django 5.0.3 on 2024-06-21 00:08

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0105_alter_tipoaccionusuario_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BitacoraAccionDteP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha')),
                ('accion', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='dte.tipoaccionusuario', verbose_name='Acción')),
                ('dte', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='dte.dteproveedor', verbose_name='DTE')),
                ('tipoDte', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='dte.tipodocumento', verbose_name='Tipo DTE')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]