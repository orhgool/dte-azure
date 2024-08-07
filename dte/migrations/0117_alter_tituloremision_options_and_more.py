# Generated by Django 5.0.3 on 2024-06-30 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0116_alter_cliente_departamento_alter_cliente_municipio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tituloremision',
            options={'ordering': ('codigo',), 'verbose_name': 'Título a que se remiten los bienes', 'verbose_name_plural': 'Títulos a que se remiten los bienes'},
        ),
        migrations.AddField(
            model_name='dtecliente',
            name='tituloRemision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dte.tituloremision', verbose_name='Título remisión'),
        ),
        migrations.AlterField(
            model_name='dteproveedordetalle',
            name='dte',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='dte.dteproveedor'),
        ),
    ]
