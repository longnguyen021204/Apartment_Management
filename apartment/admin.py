from django.contrib import admin
from .models import *
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','amount', 'payment_type', 'payment_method','payment_date','description']




admin.site.register(User)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Vehicle)
admin.site.register(LockerItem)
admin.site.register(Survey)
