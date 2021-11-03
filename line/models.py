from django.db import models
from django.db.models.base import Model, ModelState
from django.contrib.auth.models import User

# Create your models here.

class CustomUser(models.Model):
    line_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10)
    ref_friend = models.ForeignKey('CustomUser', related_name='ref', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_user_by_line_id(line_id):
        return CustomUser.objects.filter(line_id=line_id).first()

class LineOfficial(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LineLogin(models.Model):
    FORM = 1
    HISTORY = 2
    CALCULATEPRICE = 3
    RIDIRECT_CHOICES = [
        (FORM, 'FORM'),
        (HISTORY, 'HISTORY'),
        (CALCULATEPRICE, 'CALCULATEPRICE'),
    ]
    name = models.CharField(max_length=20)
    line_official = models.ForeignKey(LineOfficial, on_delete=models.CASCADE, related_name='login')
    mode = models.IntegerField(choices=RIDIRECT_CHOICES)
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

class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='model')
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def map_object_to_json(objects):
        result = []
        for model in objects:
            result.append({
                'name': model.name,
                'id': model.id
            })
        return result

class Car(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True )
    # TODO forieng key
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE,blank=True,null=True )
    car_register = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def get_car_by_id(car_id):
        return Car.objects.filter(id=car_id)
    
    def map_object_to_list(objects):
        cars = []
        for car in objects:
            cars.append({
                    # 'brand': car.brand,
                    'model': car.model,
                    'car_register': car.car_register,
                    'id': car.id
                })
        return cars

    def __str__(self):
        return str(self.id)


