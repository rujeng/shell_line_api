# Generated by Django 3.2 on 2022-07-16 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0008_auto_20220716_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertrans',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
