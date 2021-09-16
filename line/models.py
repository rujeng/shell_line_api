from django.db import models
from django.db.models.base import Model

# Create your models here.

class LineOfficial(models.Model):
    name = models.CharField(max_length=20)
    channel_id = models.CharField(max_length=20)
    channel_secrete = models.CharField(max_length=50)
    client_id = models.CharField(max_length=20)
    channel_access_token = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TransactionForm(models.Model):
    meta_data = models.TextField(blank=True, null=True)
    line_official = models.ForeignKey(LineOfficial, on_delete=models.CASCADE, )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)