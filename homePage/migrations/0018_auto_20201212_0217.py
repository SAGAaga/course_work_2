# Generated by Django 3.1 on 2020-12-12 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0017_delete_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='contract_number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='homePage.contract'),
        ),
    ]
