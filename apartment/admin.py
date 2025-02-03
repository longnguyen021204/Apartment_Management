from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header = 'Apartment Admin Site'
    site_title = 'Management System'

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id_room', 'user',]
    list_filter = ['id_room', 'user']


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email','room']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','amount', 'payment_type', 'payment_method','payment_date','description','status']
    list_filter = ['amount', 'payment_date', 'status']

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['user','vehicle_type']


admin.site = MyAdminSite(name="Apartment Management")

admin.site.register(User,MyUserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(LockerItem)
admin.site.register(Survey)
