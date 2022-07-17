# Generated by Django 3.2 on 2022-07-16 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0009_ordertrans_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertrans',
            name='distance_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]