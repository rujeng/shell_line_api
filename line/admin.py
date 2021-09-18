from django.contrib import admin
from line.models import LineLogin , LineMessage, TransactionForm
# Register your models here.

admin.site.register(LineLogin)
admin.site.register(LineMessage)
admin.site.register(TransactionForm)