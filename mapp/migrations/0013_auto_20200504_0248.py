# Generated by Django 2.2.2 on 2020-05-04 02:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mapp', '0012_auto_20200504_0146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datos_extravio',
            name='ip_dispositivo',
        ),
        migrations.AddField(
            model_name='datos_extravio',
            name='apellido_publicador',
            field=models.CharField(default='Perez', max_length=40),
        ),
        migrations.AddField(
            model_name='datos_extravio',
            name='nombre_publicador',
            field=models.CharField(default='Juan', max_length=40),
        ),
        migrations.AlterField(
            model_name='datos',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2020, 5, 4, 2, 48, 29, 5478, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='datos_adopcion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2020, 5, 4, 2, 48, 29, 7606, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='datos_extravio',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2020, 5, 4, 2, 48, 29, 9367, tzinfo=utc)),
        ),
    ]
