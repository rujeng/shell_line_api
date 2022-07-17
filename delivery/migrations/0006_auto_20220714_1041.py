# Generated by Django 3.2 on 2022-07-14 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_auto_20220714_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='avatar',
            field=models.ImageField(default=1, upload_to='menu_images'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='avatar',
            field=models.ImageField(default=1, upload_to='restaurant_images'),
            preserve_default=False,
        ),
    ]