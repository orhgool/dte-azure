# Generated by Django 5.0.1 on 2024-02-03 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dte', '0005_alter_municipio_departamento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipodocumentoidentificacion',
            options={'ordering': ('nombre',)},
        ),
        migrations.AlterModelOptions(
            name='tipodonacion',
            options={'ordering': ('codigo',), 'verbose_name': 'Tipo de donación', 'verbose_name_plural': 'Tipos de donación'},
        ),
        migrations.AlterModelOptions(
            name='tipoestablecimiento',
            options={'ordering': ('codigo',), 'verbose_name': 'Tipo de establecimiento', 'verbose_name_plural': 'Tipos de establecimiento'},
        ),
        migrations.AlterModelOptions(
            name='tipoinvalidacion',
            options={'ordering': ('codigo',), 'verbose_name': 'Tipo de invalidación', 'verbose_name_plural': 'Tipos de invalidación'},
        ),
        migrations.AlterModelOptions(
            name='tipoitem',
            options={'ordering': ('codigo',), 'verbose_name': 'Tipo de ítem', 'verbose_name_plural': 'Tipos de ítem'},
        ),
        migrations.AlterModelTable(
            name='recintofiscal',
            table='dte_recintofiscal',
        ),
    ]
