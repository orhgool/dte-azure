# Generated by Django 5.0.3 on 2024-04-13 11:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0084_dtecontingencia_numerocontrol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtecliente',
            name='fecEmi',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha de emisión'),
        ),
    ]
