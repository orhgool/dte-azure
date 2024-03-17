# Generated by Django 5.0.1 on 2024-02-07 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0013_alter_dteclientedetalle_codigodetalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtecliente',
            name='codigoGeneracion',
            field=models.CharField(db_column='codigogeneracion', default='', max_length=36, primary_key=True, serialize=False, verbose_name='Código de generación'),
        ),
        migrations.AlterField(
            model_name='dteclientedetalle',
            name='codigoDetalle',
            field=models.CharField(db_column='CodigoDetalle', default='DB73F035-29BA-49E9-896C-0F5C2707F2DC', max_length=36, primary_key=True, serialize=False),
        ),
    ]
