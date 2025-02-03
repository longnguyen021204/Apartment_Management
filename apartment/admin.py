from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header = 'Apartment Admin Site'
    site_title = 'Management System'

class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', ]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','amount', 'payment_type', 'payment_method','payment_date','description']
    list_filter = ['amount', 'payment_date', 'status']

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['user','vehicle_type']


admin.site.register(User,AdminUserAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(LockerItem)
admin.site.register(Survey)
