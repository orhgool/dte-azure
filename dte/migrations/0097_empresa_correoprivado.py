# Generated by Django 5.0.3 on 2024-06-19 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0096_alter_cliente_correo'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='correoPrivado',
            field=models.BooleanField(blank=True, default=False, verbose_name='Usar correo privado'),
        ),
    ]