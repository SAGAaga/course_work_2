# Generated by Django 3.1 on 2020-11-29 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0011_auto_20201129_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='pay_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
