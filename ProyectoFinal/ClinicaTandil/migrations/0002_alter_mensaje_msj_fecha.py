# Generated by Django 4.2.2 on 2023-07-11 11:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ClinicaTandil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='msj_fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
