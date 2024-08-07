# Generated by Django 5.0.3 on 2024-04-01 17:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0060_dtecliente_regimen'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Incoterm',
            new_name='Incoterms',
        ),
        migrations.AlterModelOptions(
            name='incoterms',
            options={'ordering': ('nombre',), 'verbose_name': 'Incoterms', 'verbose_name_plural': 'Incoterms'},
        ),
        migrations.AlterField(
            model_name='dtecliente',
            name='regimen',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='dte.regimen', verbose_name='Regimen'),
        ),
    ]
