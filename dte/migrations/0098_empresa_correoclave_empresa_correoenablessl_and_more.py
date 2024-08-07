# Generated by Django 5.0.3 on 2024-06-19 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0097_empresa_correoprivado'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='correoClave',
            field=models.CharField(default='', max_length=50, verbose_name='Clave de correo'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='correoEnableSsl',
            field=models.BooleanField(default=True, verbose_name='Utiliza SSL'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='correoPuertoSmtp',
            field=models.IntegerField(default=587, verbose_name='Puerto SMTP'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='correoServidorSmtp',
            field=models.CharField(default='', max_length=50, verbose_name='Servidor SMTP'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='correoUsuario',
            field=models.EmailField(default='usuario@empresa.com', max_length=50, verbose_name='Usuario de correo'),
        ),
    ]
