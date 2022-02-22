from rest_framework import serializers
from Models.models import *
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

class Roleserializer(serializers.ModelSerializer):
    class Meta():
        model = Role
        fields = '__all__'
class Forgotpasswordserilaizers(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number',)

class passwordresetserializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fileds = ('id','mobile_number')

class LoginSerializer(serializers.Serializer):

    mobile_number = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    tokens = serializers.SerializerMethodField()

    is_otpvalidated = serializers.SerializerMethodField()

    role = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(mobile_number=obj['mobile_number'])

        return ( user.tokens()['access'])
    def get_is_otpvalidated(self, obj):
        user = User.objects.get(mobile_number=obj['mobile_number'])

        return (user.is_otpvalidated)

    def get_role(self,obj):
        user = User.objects.get(mobile_number=obj['mobile_number'])

        return (user.role)

    def validate(self, attrs):
        mobile_number = attrs.get('mobile_number', '')
        password = attrs.get('password', '')
        filtered_user_by_mobile_number = User.objects.filter(mobile_number=mobile_number)
        user = auth.authenticate(mobile_number=mobile_number, password=password)

        if not user:
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_404_NOT_FOUND,'detail': 'Invalid credentials, try again'})

        return {
            'mobile_number': user.mobile_number,
            'is_otpvalidated': user.is_otpvalidated,
            'tokens': user.tokens,
            'role' : user.role
        }

        return super().validate(attrs)

class Getallusers(serializers.ModelSerializer):

    class Meta():
        model =User
        fields = ('id','mobile_number','email','full_name','is_verified','is_paymentdone','is_formupdated','payment_verified','is_otpvalidated','payment_photo','role_id','role','talukhead_id','statehead_id','districthead_id','assigned_stateid','assigned_talukid','assigned_districtid')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number','email','password','full_name','role')
        extra_kwargs = {'password':{"write_only":True,'required':True}}

class Profileserializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number','email','full_name','profile_photo')

class FormsSerializer(serializers.ModelSerializer):

    class Meta():
        model = Form
        exclude = ('createdby','updated_on')

class FormSerializer(serializers.ModelSerializer):

    class Meta():
        model = Form
        exclude = ('createdby','form_verified','updated_on')

class PaymentSerializer(serializers.ModelSerializer):

    class Meta():
        model = Payment
        exclude = ('id','state')

class AttendenceSerializer(serializers.ModelSerializer):

    class Meta():
        model = Attendence
        exclude = ('id','user_id')

class Formapproveserializer(serializers.ModelSerializer):

    class Meta():
        model = Form
        fields =('mobile','form_verified')

class Getpaymentdetailserializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number','email','full_name','payment_photo')

class Updatepaymentdetials(serializers.ModelSerializer):
    class Meta():
        model = Payment
        exclude = ('id','state')
class PostPaymentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Payment
        exclude = ('id',)

class Verifyuserserializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number','is_verified')

class Userstatusserializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number','is_otpvalidated','is_formupdated','is_paymentdone')

class Paymentverifyuserserializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number','payment_verified')

class Formverifyuserserializer(serializers.ModelSerializer):
    class Meta():

        model = User
        fields = ('mobile_number','form_verified')

class Upload_profilephoto(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('profile_photo',)

class Upload_Qrphoto(serializers.ModelSerializer):
    class Meta():
        model = Payment
        fields = ('qr_code','state_id')
class RequestupdateformSerializer(serializers.ModelSerializer):

    class Meta():
        model = Form
        fields =('mobile',)


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'role': self.user.role})
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class GetallWorkerserializer(serializers.ModelSerializer):
    class Meta():
        model =User
        fields = ('mobile_number','email','full_name','role')

class DeleteRoleserializer(serializers.ModelSerializer):
    class Meta():
        model = Role
        fields = ('id',)

class Districtserializer(serializers.ModelSerializer):
        class Meta():
            model = District_master
            fields = ('id','district_name')


class CreateRoleserializer(serializers.ModelSerializer):
    class Meta():
        model = Role
        fields = ('rolename',)

class Createstateserializer(serializers.ModelSerializer):
    class Meta():
        model = State_master
        fields = ('id','state_name')

class AssignRoleserializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('mobile_number','role_id','talukhead_id','statehead_id','districthead_id','assigned_stateid','assigned_districtid','assigned_talukid')

class Getallstateheadserializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ('full_name','id','email','mobile_number','designation_id')

class Deletestateserializer(serializers.ModelSerializer):
    class Meta():
        model = State_master
        fields = ('id',)

class Talukserializer(serializers.ModelSerializer):

    class Meta():
        model = Taluk_master
        fields = ('id','taluk_name')


class Getallattendanceserilaizers(serializers.ModelSerializer):

    class Meta():
        model = Attendence
        fields = ('status','date')

class Deleteformserilaizers(serializers.ModelSerializer):
    class Meta():
        model = Form
        fields = ('mobile',)   
