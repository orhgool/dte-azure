# Generated by Django 5.0.3 on 2024-04-01 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0059_alter_dtecliente_recintofiscal_alter_regimen_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='dtecliente',
            name='regimen',
            field=models.ForeignKey(blank=True, default='EX-1.1000.000', null=True, on_delete=django.db.models.deletion.CASCADE, to='dte.regimen', verbose_name='Regimen'),
        ),
    ]
