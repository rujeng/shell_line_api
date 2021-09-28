from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User

# Create your models here.

class CustomeUser(models.Model):
    line_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=10)
    ref_friend = models.ForeignKey('CustomeUser', related_name='ref', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.first_name else '---'

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

class TransactionForm(models.Model):
    INITIAL = '1'
    PROCESSING = '2'
    DONE = '3'
    FAILED = '4'
    STATUS_CHOICES = [
        (INITIAL, 'INITIAL'),
        (PROCESSING, 'PROCESSING'),
        (DONE, 'DONE'),
        (FAILED, 'FAILED'),
    ]
    branch_id = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, blank=True,null=True)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=INITIAL)
    appointed_date = models.DateTimeField()
    price = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}' if self.user_id.first_name else '---' 

class  Car(models.Model):
    CARS = [
        {'id': 1, 'brand': 'isuzu'},
        {'id': 2, 'brand': 'hyundai'},
        {'id': 3, 'brand': 'mazda'},
        {'id': 4, 'brand': 'nissan'},
        {'id': 5, 'brand': 'suzuki'},
        {'id': 6, 'brand': 'subaru'},
        {'id': 7, 'brand': 'toyota'},
    ]
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE,blank=True,null=True )
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    car_register = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# class User(models.Model):
#       phone = models.CharField(max_length=20)
#       line_id = models.CharField(max_length=20)
#       ref_friend = models.CharField(max_length=20)
#       updated_by = models.CharField(max_length=20)
#       updated_date = models.CharField(max_length=20)
#       created_date = models.CharField(max_length=20)
