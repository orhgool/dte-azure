# Generated by Django 5.0.1 on 2024-03-15 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0039_alter_empresa_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(blank=True, db_column='Nombre', max_length=200, null=True),
        ),
    ]
