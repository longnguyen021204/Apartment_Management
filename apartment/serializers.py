
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

# USER #
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'avatar', 'password', 'is_resident')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['old_password'] != attrs['new_password']:
            raise serializers.ValidationError({'old_password': '<PASSWORD>.'})


# PAYMENTS #
class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Payment
        fields = ['amount','payment_type', 'payment_date', 'user']
        extra_kwargs = {'user': {'read_only': True}}


# VEHICLES #
class VehicleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'brand', 'model']

# LockerItem #
class LockerItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = LockerItem
        fields = ['item_name', 'locker_number', 'received_date', 'status']

# FEEDBACK #
class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Feedback
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Survey
        fields = '__all__'