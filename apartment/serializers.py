
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

# USER #
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name','email','username', 'password','avatar')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
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
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Payment
        fields = ['user','amount','payment_type', 'payment_date']
        extra_kwargs = {'user': {'read_only': True}}


# VEHICLES #
class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Vehicle
        fields = ['user','vehicle_type', 'brand', 'model']
        extra_kwargs = {'user': {'read_only': True}}

# LockerItem #
class LockerItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LockerItem
        fields = ['user','locker_number','item_name', 'received_date', 'status']
        extra_kwargs = {'user': {'read_only': True}}

# FEEDBACK #
class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
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