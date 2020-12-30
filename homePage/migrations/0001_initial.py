# Generated by Django 3.1 on 2020-11-27 21:51

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accomodation',
            fields=[
                ('accomodation_id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=255)),
                ('squeare', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_number', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(code='Incorrect length', message='Length has to be 8', regex='^\\d{8}$')])),
                ('last_date_of_prolongation', models.DateField(auto_now=True)),
                ('term', models.DateField(default=datetime.date(2021, 5, 27))),
                ('is_activ', models.BooleanField(default=True)),
                ('accomodation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homePage.accomodation')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tarif',
            fields=[
                ('tarif_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('bottom_line', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('top_line', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Tarif_Accomodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accomodation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homePage.accomodation')),
                ('tarif_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homePage.tarif')),
            ],
        ),
        migrations.AddField(
            model_name='tarif',
            name='accomodation',
            field=models.ManyToManyField(through='homePage.Tarif_Accomodation', to='homePage.Accomodation'),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('consumed', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('debt', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('prepayment', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('accomodation_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='homePage.accomodation')),
            ],
        ),
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