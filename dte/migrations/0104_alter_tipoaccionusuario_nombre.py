# Generated by Django 5.0.3 on 2024-06-21 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0103_bitacoraacciondtec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoaccionusuario',
            name='nombre',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Nombre'),
        ),
    ]
