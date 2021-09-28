from django.contrib import admin
from line.models import LineLogin , LineMessage, TransactionForm, CustomeUser, Car, LineOfficial
# Register your models here.

admin.site.register(LineLogin)
admin.site.register(LineMessage)
# admin.site.register(TransactionForm)
admin.site.register(CustomeUser)
admin.site.register(LineOfficial)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'user_id', 'car_register')


@admin.register(TransactionForm)
class TransactionFormrAdmin(admin.ModelAdmin):
    list_display = ('brand', 'user_id', 'status')

    def brand(self, obj):
        car = Car.objects.filter(id=obj.car_id).first()
        if car:
            return car.brand
        return '--'
