from datetime import datetime
from urllib import request

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

# ROOM #
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

# USER #
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name','email','username', 'password','avatar','room')
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
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    # user = UserSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['user_id','amount','payment_type', 'payment_date','status']
        extra_kwargs = {'user_id': {'read_only': True}}

class PaymentDetailSerializer(PaymentSerializer):
    payment_details = PaymentSerializer(many=True, read_only=True)
    class Meta:
        fields = PaymentSerializer.Meta.fields + ['payment_details']

    def get_vnpay_url(self, obj):
        from apartment.vnpay import vnpay  # Import class VNPay đã cấu hình
        vnPay = vnpay()
        order_type = 'other'
        order_id = str(obj.id)
        amount = sum([details.amount for details in obj.payment_details.all()])
        order_desc = f"{order_id}"
        ipaddr = self.context.get('request').META.get('REMOTE_ADDR')
        if not ipaddr:
            ipaddr = self.context.get('request').META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0]
        # Build URL Payment
        vnp = vnpay()
        vnp.requestData['vnp_Version'] = '2.1.0'
        vnp.requestData['vnp_Command'] = 'pay'
        vnp.requestData['vnp_TmnCode'] = settings.VNP_TMNCODE
        vnp.requestData['vnp_Amount'] = int(amount * 100)
        vnp.requestData['vnp_CurrCode'] = 'VND'
        vnp.requestData['vnp_TxnRef'] = order_id
        vnp.requestData['vnp_OrderInfo'] = order_desc
        vnp.requestData['vnp_OrderType'] = order_type
        vnp.requestData['vnp_Locale'] = 'vn'
        vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
        vnp.requestData['vnp_IpAddr'] = ipaddr
        vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
        vnpay_payment_url = vnp.get_payment_url(settings.VNP_URL, settings.VNP_HASHSECRET)

        return vnpay_payment_url

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

class ItemSerializer(serializers.ModelSerializer):
    locker = LockerItemSerializer(read_only=True)
    class Meta:
        model = Item
        fields = '__all__'


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