# Generated by Django 5.0.3 on 2024-04-10 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0079_remove_dtecontingenciadetalle_tipodte'),
    ]

    operations = [
        migrations.AddField(
            model_name='dtecontingenciadetalle',
            name='tipoDte',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dte.tipodocumentocontingencia', verbose_name='Tipo DTE'),
        ),
    ]