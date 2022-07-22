# Generated by Django 3.2 on 2022-07-20 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0011_auto_20220717_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('detail', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='menudetail',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
