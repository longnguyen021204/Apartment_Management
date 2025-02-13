from django.contrib.auth import user_logged_in
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework import status
from cloudinary.models import CloudinaryField

class Room(models.Model):
    id_room = models.AutoField(primary_key=True, unique=True, editable=False)
    user = models.OneToOneField('User', null=True, on_delete=models.SET_NULL, blank=True,
                                      related_name='room')

    def __str__(self):
        return f"{self.id_room}"

class User(AbstractUser):
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    avatar = CloudinaryField('avatars', null=True, blank=True)
    is_resident = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=255)  # Ví dụ: "Phí quản lý", "Phí gửi xe"
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    # payment_image = models.ImageField(upload_to='payment_images/', null=True, blank=True)
    payment_image = CloudinaryField('payment_img', null=True, blank=True)

    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        if status:
            return f"Payment {self.id} by {self.user}"

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)  # Ví dụ: "Ô tô", "Xe máy"
    brand = models.CharField(max_length=50, null=True, blank=True)  # Ví dụ: "Toyota", "Honda"
    model = models.CharField(max_length=50, null=True, blank=True)  # Ví dụ: "Vios", "SH"

    def __str__(self):
        return self.vehicle_type

class LockerItem(models.Model):
    id_locker = models.AutoField(primary_key=True, unique=True, editable=False,)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='locker_user', null=True, blank=True)
    def __str__(self):
        return f"{self.id_locker}"

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    received_date = models.DateTimeField(auto_now_add=True)
    pickup_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default="Chờ nhận")
    lockeritem = models.ForeignKey(LockerItem, on_delete=models.CASCADE, null=True,
                                      blank=True)

    def __str__(self):
        return self.item_name

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback created by {self.user} at {self.created_at}"


class Survey(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers_given')
    text = models.TextField()

    def __str__(self):
        return self.text