# Generated by Django 3.1 on 2021-01-02 23:09

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0020_auto_20201212_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='date_in',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contract',
            name='term',
            field=models.DateField(default=datetime.date(2021, 7, 2)),
        ),
    ]
