# Generated by Django 5.0.1 on 2024-03-09 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0036_alter_dteclientedetalletributo_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='nrc',
            field=models.CharField(blank=True, db_column='NRC', default='', max_length=10, null=True, verbose_name='NRC'),
        ),
    ]
