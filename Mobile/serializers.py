from rest_framework import serializers
from Models.models import *
from rest_framework import serializers
from .models import *
from django.contrib import auth
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg import openapi
from rest_framework.schemas import AutoSchema

class SignupSerializer(serializers.ModelSerializer):

    class Meta():

        model = User
        fields = ('email','password','mobile_number','full_name','state_id','district_id','taluk_id')
        extra_kwargs = {'password':{"write_only":True,'required':True}}

class ProfileSerializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('id','mobile_number','email','full_name','profile_photo')

class GetPaymentSerializer(serializers.ModelSerializer):

    class Meta():

        model = Payment
        exclude = ('id',)

class Photoserializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('profile_photo',)

class Forgotpasswordserilaizer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number',)


class Otp_ResendSerializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number',)

class Formverify(serializers.ModelSerializer):
    class Meta():

        model = Form
        fields = ('form_verified',)

class Check_verifiedserializer(serializers.ModelSerializer):
    form_verified = serializers.BooleanField(default=False)
    class Meta():
        model = User
        fields = ('is_verified','is_formupdated','is_paymentdone','is_otpvalidated','form_verified')

class Sampleviewserializer(serializers.ModelSerializer):

    class Meta():
        model = Sample
        fields = '__all__'

class Otp_validateSerializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('otp','mobile_number')

class PaymentSerializer(serializers.ModelSerializer):

    class Meta():
        model = Payment
        exclude = ('id',)

class upload_screenshot(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('payment_photo',)

class FormSerializer(serializers.ModelSerializer):

    class Meta():
        model = Form
        exclude = ('id','createdby','form_verified','updated_on')

class PaymentSerializer(serializers.ModelSerializer):

    class Meta():
        model = Payment
        exclude = ('id',)

class AttendenceSerializer(serializers.ModelSerializer):

    class Meta():
        model = Attendence
        exclude = ('id','user_id')

class Checkattendence(serializers.ModelSerializer):

    class Meta():
        model = Attendence
        fields = ('date',)

class Stateserializer(serializers.ModelSerializer):
    class Meta():
        model = State_master
        fields = ('id','state_name')

class Districtserializer(serializers.ModelSerializer):
        class Meta():
            model = District_master
            fields = ('id','district_name')
            
class TaluksSerializer(serializers.ModelSerializer):
        class Meta():
            model = Taluk_master
            fields = ('id','taluk_name')
            
class Popupserializer(serializers.ModelSerializer):
        class Meta():
            model = User
            fields = ('state_id','district_id','taluk_id')

class upload_document(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('document_photo',)
