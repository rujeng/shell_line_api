from django.db import models
from django.db.models.base import Model

# Create your models here.

class LineLogin(models.Model):
    name = models.CharField(max_length=20)
    branch_id = models.CharField(max_length=20)
    channel_secret = models.CharField(max_length=50)
    channel_id = models.CharField(max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LineMessage(models.Model):
    name = models.CharField(max_length=20)
    branch_id = models.CharField(max_length=20)
    channel_access_token = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name        

class TransactionForm(models.Model):
    meta_data = models.TextField(blank=True, null=True)
    line_message = models.ForeignKey(LineMessage, on_delete=models.CASCADE,blank=True,null=True )
    user_id = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id       