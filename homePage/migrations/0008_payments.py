# Generated by Django 3.1 on 2020-11-28 23:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0007_auto_20201129_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('summ', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('pay_datetime', models.DateTimeField(auto_now_add=True)),
                ('contract_number', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='homePage.contract')),
            ],
        ),
    ]