from django.contrib import admin
from otp.models import OtpRequest
# Register your models here.
# admin.site.register(OtpRequest)

@admin.register(OtpRequest)
class OtpRequestrAdmin(admin.ModelAdmin):
    list_display = ('ref_code', 'mobile_no', 'count')