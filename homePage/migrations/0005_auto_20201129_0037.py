# Generated by Django 3.1 on 2020-11-28 22:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0004_auto_20201128_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='last_date_of_prolongation',
            field=models.DateField(default=datetime.date(2020, 11, 29)),
        ),
        migrations.AlterField(
            model_name='contract',
            name='term',
            field=models.DateField(default=datetime.date(2021, 5, 29)),
        ),
    ]
