from django.contrib import admin
from line.models import CarModel, LineLogin , LineMessage, CustomUser, Car, LineOfficial , CarBrand
# Register your models here.

admin.site.register(LineLogin)
admin.site.register(LineMessage)
admin.site.register(LineOfficial)
admin.site.register(CarBrand)
admin.site.register(CarModel)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'user_id', 'car_register')
    search_fields = ('car_register', 'user_id__id')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'full_name', )
    search_fields = ('mobile_no', 'id')


