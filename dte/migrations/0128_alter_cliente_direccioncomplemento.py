# Generated by Django 5.0.3 on 2024-07-16 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0127_alter_cliente_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='direccionComplemento',
            field=models.CharField(blank=True, db_column='Direccion', max_length=200, null=True, verbose_name='Dirección'),
        ),
    ]
