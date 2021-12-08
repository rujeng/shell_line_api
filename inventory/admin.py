from django.contrib import admin
from inventory.models import Inventory, InventoryCount, InventoryDetail
# Register your models here.

admin.site.register(Inventory)
admin.site.register(InventoryCount)
admin.site.register(InventoryDetail)