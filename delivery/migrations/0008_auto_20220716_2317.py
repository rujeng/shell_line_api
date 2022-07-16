# Generated by Django 3.2 on 2022-07-16 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_ordertrans_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertrans',
            name='branch_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordertrans',
            name='status',
            field=models.CharField(choices=[('1', 'INITIAL'), ('2', 'PROCESSING'), ('3', 'CONFIRM'), ('4', 'DONE'), ('5', 'FAILED')], default='1', max_length=10),
        ),
    ]
