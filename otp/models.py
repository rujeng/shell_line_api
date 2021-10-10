from django.db import models

# Create your models here.

class OtpRequest(models.Model):
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, related_name='user_transaction')
    line_id = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=20)
    ref_code = models.CharField(max_length=10)
    token = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)