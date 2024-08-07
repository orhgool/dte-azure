# Generated by Django 5.0.3 on 2024-07-08 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0118_alter_dteclientedetalle_preciouni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtecliente',
            name='totalGravada',
            field=models.DecimalField(blank=True, decimal_places=4, default=0.0, max_digits=18, null=True, verbose_name='Total gravadas'),
        ),
        migrations.AlterField(
            model_name='dteclientedetalle',
            name='ventaGravada',
            field=models.DecimalField(db_column='VentaGravada', decimal_places=4, default=0, max_digits=11, verbose_name='Venta gravada'),
        ),
    ]
