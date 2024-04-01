# Generated by Django 5.0.3 on 2024-03-30 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0051_remove_configuracion_enablessl_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracion',
            name='puerto_smtp',
        ),
        migrations.RemoveField(
            model_name='configuracion',
            name='smtp',
        ),
        migrations.AddField(
            model_name='configuracion',
            name='puertoSmtp',
            field=models.IntegerField(default=587, verbose_name='Puerto SMTP'),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='servidorSmtp',
            field=models.CharField(default='', max_length=500, verbose_name='Servidor SMTP'),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='claveCorreo',
            field=models.CharField(default='', max_length=500, verbose_name='Clave de correo'),
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='usuarioCorreo',
            field=models.EmailField(default='none@usuario.com', max_length=500, verbose_name='Usuario de correo'),
        ),
    ]
