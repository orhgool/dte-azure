# Generated by Django 5.0.3 on 2024-04-02 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0063_alter_pais_options_dtecliente_totalcompra_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dteclientedetalletributo',
            old_name='codigoDetalle',
            new_name='codigodetalle',
        ),
    ]
