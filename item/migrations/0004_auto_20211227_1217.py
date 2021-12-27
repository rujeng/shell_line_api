# Generated by Django 2.2.10 on 2021-12-27 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_transactionform_is_notify'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionform',
            name='is_notify_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transactionform',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('CASH', 'เงินสด'), ('TRANSFER_BBL', 'โอน_BBL'), ('CREDIT_CARD_SCB', 'เครดิตการ์ด_SCB'), ('QR_SCB', 'QR_SCB'), ('CUSTOMER_CREDIT', 'ลูกค้าเครดิต')], max_length=20, null=True),
        ),
    ]
