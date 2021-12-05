from django.db import models
from django.db.models import indexes

# Create your models here.

class Inventory(models.Model):
    shipment_number = models.CharField(max_length=50)
    delivery_number = models.CharField(max_length=50)
    reference_order = models.CharField(max_length=50)
    storage = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InventoryDetail(models.Model):
    inventory = models.ForeignKey('Inventory', related_name='detail', on_delete=models.CASCADE)
    item = models.ForeignKey('item.Item', on_delete=models.CASCADE)
    shipment_number = models.CharField(max_length=50)
    delivery_number = models.CharField(max_length=50)
    reference_order = models.CharField(max_length=50)

    order = models.CharField(max_length=50)
    product = models.CharField(max_length=50)

    quantity = models.IntegerField(default=0)
    total_bill = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InventoryCount(models.Model):
    item = models.ForeignKey('item.Item', on_delete=models.CASCADE)
    inventory_barcode = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, db_index=True)
    amount = models.IntegerField(default=0)
    storage = models.CharField(max_length=50, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)