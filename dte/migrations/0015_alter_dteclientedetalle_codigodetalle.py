# Generated by Django 5.0.1 on 2024-02-07 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0014_alter_dtecliente_codigogeneracion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dteclientedetalle',
            name='codigoDetalle',
            field=models.CharField(db_column='CodigoDetalle', default='A3BF0F8A-04FC-47D2-80B6-9FD338EC6394', max_length=36, primary_key=True, serialize=False),
        ),
    ]
