# Generated by Django 5.0.3 on 2024-04-10 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0074_alter_dtecontingencia_tipodte'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dtecontingencia',
            name='tipoDte',
        ),
    ]