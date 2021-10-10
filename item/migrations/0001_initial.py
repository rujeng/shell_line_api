# Generated by Django 2.2.2 on 2021-09-30 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('line', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_barcode', models.CharField(max_length=20)),
                ('barcode', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('supplier', models.CharField(max_length=50)),
                ('main_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('sell_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('image_url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_id', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('1', 'INITIAL'), ('2', 'PROCESSING'), ('3', 'DONE'), ('4', 'FAILED')], default='1', max_length=10)),
                ('appointed_date', models.DateTimeField()),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_transaction', to='line.Car')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_transaction', to='line.CustomUser')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('sell_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('location_store', models.CharField(max_length=30)),
                ('comment', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='item.Item')),
                ('transaction_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_detail', to='item.TransactionForm')),
            ],
        ),
    ]
