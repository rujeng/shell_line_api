# Generated by Django 2.2.2 on 2021-12-04 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_orderdetail_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]