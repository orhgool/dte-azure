# Generated by Django 5.0.1 on 2024-02-27 10:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0031_alter_empresa_actividadeconomica_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='tipoEstablecimiento',
            field=models.ForeignKey(default='01', on_delete=django.db.models.deletion.CASCADE, to='dte.tipoestablecimiento', verbose_name='Tipo de establecimiento'),
        ),
    ]
