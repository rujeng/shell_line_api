from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User

# Create your models here.

class CustomUser(models.Model):
    line_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10)
    ref_friend = models.ForeignKey('CustomUser', related_name='ref', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class LineOfficial(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LineLogin(models.Model):
    name = models.CharField(max_length=20)
    line_official = models.ForeignKey(LineOfficial, on_delete=models.CASCADE, related_name='login')
    channel_secret = models.CharField(max_length=50)
    channel_id = models.CharField(max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LineMessage(models.Model):
    name = models.CharField(max_length=20)
    line_official = models.ForeignKey(LineOfficial, on_delete=models.CASCADE, related_name='message')
    channel_access_token = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name        

class CarBrand(models.Model):
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class  Car(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True )
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    car_register = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def map_object_to_list(objects):
        cars = []
        for car in objects:
            cars.append({
                    'brand': car.brand,
                    'model': car.model,
                    'car_register': car.car_register,
                    'id': car.id
                })
        return cars

    def __str__(self):
        return str(self.id)


