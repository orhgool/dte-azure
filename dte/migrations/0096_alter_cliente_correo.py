# Generated by Django 5.0.3 on 2024-06-19 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0095_alter_dtecontingencia_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='correo',
            field=models.CharField(db_column='Correo', default='', max_length=200, verbose_name='Correo'),
        ),
    ]
