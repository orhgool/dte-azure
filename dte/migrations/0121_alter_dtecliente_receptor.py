# Generated by Django 5.0.3 on 2024-07-10 05:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0120_alter_dtecliente_ivaperci1_alter_dtecliente_ivarete1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtecliente',
            name='receptor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dte.cliente'),
        ),
    ]
