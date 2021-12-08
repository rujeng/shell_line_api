from django.contrib import admin
from item.models import Item, TransactionForm, TransactionDetail , CalculatePrice, ItemImage
# from line.models import Car
# Register your models here.

admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(TransactionDetail)

@admin.register(TransactionForm)
class TransactionFormrAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'status')

    def brand(self, obj):
        car = obj.car.id
        if car:
            return car

        return '--'

@admin.register(CalculatePrice)
class CalculatePricerAdmin(admin.ModelAdmin):
    list_display = ('name','series','status')