# Generated by Django 5.0.3 on 2024-04-06 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0067_dteinvalidacion_docfirmado_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dteinvalidacion',
            old_name='fechaEmimision',
            new_name='fechaEmision',
        ),
    ]
