# Generated by Django 2.2.2 on 2021-11-03 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line', '0004_car_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_register',
            field=models.CharField(max_length=50),
        ),
    ]
