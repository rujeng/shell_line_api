from django.contrib import admin

from delivery.models import MenuDetail, Restaurant, OrderTrans, OrderDetail, Menu, LocationUser
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(MenuDetail)
admin.site.register(LocationUser)

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('menu', 'quantity', 'ordertrans')

@admin.register(OrderTrans)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status')