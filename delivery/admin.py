from django.contrib import admin

from delivery.models import Restaurant, Order, OrderDetail, Menu
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Order)
# admin.site.register(OrderDetail)
admin.site.register(Menu)

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('menu', 'quantity', 'order')