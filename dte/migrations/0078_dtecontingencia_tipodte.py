# Generated by Django 5.0.3 on 2024-04-10 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0077_remove_dtecontingencia_tipodte'),
    ]

    operations = [
        migrations.AddField(
            model_name='dtecontingencia',
            name='tipoDte',
            field=models.ForeignKey(default='03', on_delete=django.db.models.deletion.CASCADE, to='dte.tipodocumento', verbose_name='Tipo DTE'),
        ),
    ]