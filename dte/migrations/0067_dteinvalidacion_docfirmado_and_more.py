# Generated by Django 5.0.3 on 2024-04-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0066_dteinvalidacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='dteinvalidacion',
            name='docfirmado',
            field=models.TextField(blank=True, db_column='DocFirmado', null=True, verbose_name='Documento firmado'),
        ),
        migrations.AddField(
            model_name='dteinvalidacion',
            name='selloRecepcion',
            field=models.CharField(default='', max_length=50, verbose_name='Código DTE a anular'),
        ),
    ]
