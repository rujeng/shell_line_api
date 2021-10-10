from django.contrib import admin
from line.models import LineLogin , LineMessage, CustomUser, Car, LineOfficial , CarBrand
# Register your models here.

admin.site.register(LineLogin)
admin.site.register(LineMessage)
admin.site.register(LineOfficial)
admin.site.register(CarBrand)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'user_id', 'car_register')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_no', 'full_name', )


