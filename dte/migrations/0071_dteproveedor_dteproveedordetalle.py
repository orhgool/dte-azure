# Generated by Django 5.0.3 on 2024-04-09 13:21

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0070_dtecontingenciadetalle'),
    ]

    operations = [
        migrations.CreateModel(
            name='DTEProveedor',
            fields=[
                ('version', models.IntegerField(default=3, verbose_name='Versión JSON')),
                ('numeroControl', models.CharField(blank=True, default='', max_length=31, verbose_name='Número de control')),
                ('codigoGeneracion', models.CharField(default='', max_length=36, primary_key=True, serialize=False, verbose_name='Código de generación')),
                ('selloRecepcion', models.CharField(blank=True, default='', max_length=100, verbose_name='Sello de recepción')),
                ('motivoContin', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Motivo de contingencia')),
                ('fecEmi', models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha de emisión')),
                ('totalSujetoRetencion', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=18, null=True, verbose_name='Total sujeto retención')),
                ('totalIVARetenido', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=18, null=True, verbose_name='Total IVA Retenido')),
                ('docfirmado', models.TextField(blank=True, null=True, verbose_name='Documento firmado')),
                ('ambiente', models.ForeignKey(default='00', on_delete=django.db.models.deletion.CASCADE, to='dte.ambientedestino', verbose_name='Ambiente de trabajo')),
                ('emisor', models.ForeignKey(default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837', on_delete=django.db.models.deletion.CASCADE, to='dte.empresa')),
                ('estadoDte', models.ForeignKey(blank=True, default='001', on_delete=django.db.models.deletion.CASCADE, to='dte.estadodte', verbose_name='Estado del DTE')),
                ('receptor', models.ForeignKey(default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837', on_delete=django.db.models.deletion.CASCADE, to='dte.proveedor')),
                ('tipoContingencia', models.ForeignKey(blank=True, db_column='TipoContingencia', max_length=10, null=True, on_delete=django.db.models.deletion.CASCADE, to='dte.tipocontingencia', verbose_name='Tipo de contingencia')),
                ('tipoDte', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='dte.tipodocumento', verbose_name='Tipo DTE')),
                ('tipoModelo', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='dte.modelofacturacion', verbose_name='Tipo de modelo')),
                ('tipoMoneda', models.ForeignKey(default='001', on_delete=django.db.models.deletion.CASCADE, to='dte.moneda')),
                ('tipoTransmision', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='dte.tipotransmision', verbose_name='Tipo de transmisión')),
            ],
            options={
                'verbose_name': 'DTE de proveedor',
                'verbose_name_plural': "DTE's de proveedor",
                'ordering': ('-fecEmi',),
            },
        ),
        migrations.CreateModel(
            name='DTEProveedorDetalle',
            fields=[
                ('codigoDetalle', models.CharField(default='', max_length=36, primary_key=True, serialize=False)),
                ('numeroDocumento', models.CharField(blank=True, default='', max_length=50, verbose_name='Número de documento')),
                ('fechaEmision', models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha de emisión')),
                ('montoSujetoGrav', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Monto sujeto gravado')),
                ('ivaRetenido', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='IVA retenido')),
                ('codigoRetencionMH', models.ForeignKey(default='C4', on_delete=django.db.models.deletion.CASCADE, to='dte.retencionivamh', verbose_name='Código retención MH')),
                ('dte', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='dte.dteproveedor')),
                ('tipoDte', models.ForeignKey(default='03', on_delete=django.db.models.deletion.CASCADE, to='dte.tipodocumento', verbose_name='Tipo DTE')),
                ('tipoGeneracion', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='dte.tipogeneraciondocumento', verbose_name='Tipo de generación')),
            ],
            options={
                'verbose_name': 'DTE proveedor detalle',
                'verbose_name_plural': "DTE's proveedor detalles",
            },
        ),
    ]
