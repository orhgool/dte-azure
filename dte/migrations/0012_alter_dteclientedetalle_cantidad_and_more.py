# Generated by Django 5.0.1 on 2024-02-04 13:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0011_alter_userprofile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dteclientedetalle',
            name='cantidad',
            field=models.DecimalField(blank=True, db_column='Cantidad', decimal_places=2, default=1, max_digits=11, verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='dteclientedetalle',
            name='dte',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='dte.dtecliente'),
        ),
    ]
