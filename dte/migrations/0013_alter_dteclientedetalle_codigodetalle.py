# Generated by Django 5.0.1 on 2024-02-07 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0012_alter_dteclientedetalle_cantidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dteclientedetalle',
            name='codigoDetalle',
            field=models.CharField(db_column='CodigoDetalle', default='4BEEA0B9-DEB6-44E6-97BA-1117787A67B9', max_length=36, primary_key=True, serialize=False),
        ),
    ]
