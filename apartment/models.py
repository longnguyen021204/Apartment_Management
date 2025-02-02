
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework import status


class Room(models.Model):
    id_room = models.AutoField(primary_key=True)
    user = models.OneToOneField('User', null=True, on_delete=models.PROTECT, blank=True,
                                      related_name='phong')

    def __str__(self):
        return self.id_room

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_resident = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=255)  # Ví dụ: "Phí quản lý", "Phí gửi xe"
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_image = models.ImageField(upload_to='payment_images/', null=True,
                                      blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        if status:
            return f"Payment {self.id} by {self.user}"


class Vehicle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    license_plate = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)  # Ví dụ: "Ô tô", "Xe máy"
    brand = models.CharField(max_length=50, null=True, blank=True)  # Ví dụ: "Toyota", "Honda"
    model = models.CharField(max_length=50, null=True, blank=True)  # Ví dụ: "Vios", "SH"

    def __str__(self):
        return self.license_plate


class LockerItem(models.Model):
    item_name = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=255)
    locker_number = models.CharField(max_length=20)  # Số tủ
    received_date = models.DateTimeField(auto_now_add=True)
    pickup_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default="Chờ nhận")  # Ví dụ: "Chờ nhận", "Đã nhận"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='locker_items', null=True,
                             blank=True)

    def __str__(self):
        return self.item_name


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user} at {self.created_at}"


class Survey(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='surveys_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers_given')
    text = models.TextField()

    def __str__(self):
        return self.text