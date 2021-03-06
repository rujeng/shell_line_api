from django.contrib import admin

from delivery.models import MenuDetail, Restaurant, Order, OrderDetail, Menu
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(MenuDetail)


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('menu', 'quantity', 'order')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status')