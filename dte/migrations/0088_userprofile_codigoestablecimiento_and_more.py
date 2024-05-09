# Generated by Django 5.0.3 on 2024-05-09 18:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0087_rename_tipodocumentocliente_proveedor_tipodocumentoproveedor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='codigoEstablecimiento',
            field=models.CharField(blank=True, db_column='codigoEstablecimiento', default='0000', max_length=4, null=True, verbose_name='Código de establecimiento'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='codigoPuntoVenta',
            field=models.CharField(blank=True, db_column='codigoPuntoVenta', default='0000', max_length=4, null=True, verbose_name='Código de punto de venta'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tipoEstablecimiento',
            field=models.ForeignKey(default='02', on_delete=django.db.models.deletion.CASCADE, to='dte.tipoestablecimiento', verbose_name='Tipo de establecimiento'),
        ),
    ]