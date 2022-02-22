from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,viewsets, views,generics,status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from django.contrib.auth import get_user_model
from .serializers import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .otp import send_otp
import random
import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class Sampleview(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Sampleviewserializer
    http_method_names = ['post']

    def create(self,request):
        data = request.data
        update = Sample.objects.create(is_boolean=data['is_boolean'])
        mydata = {'data':'User successfully created','code':status.HTTP_201_CREATED,'detail':'Success'}
        return Response(mydata)

from django.utils.decorators import method_decorator
class Signupviewset(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer
    http_method_names = ['post']
    def create(self,request):
        data = request.data
        mobile_number=data['mobile_number']
        email = data['email']
        check =get_user_model().objects.filter(mobile_number=mobile_number).exists()
        check1 = get_user_model().objects.filter(email=email).exists() 
        if check == False and check1 == False :
            otp = random.randint(1000,9999)
            res = send_otp(mobile_number,otp)
            statedata = list(State_master.objects.filter(id=data['state_id']).values())
            statename = ''
            districtname = ''
            talukname = ''
            for c in statedata:
                statename = c['state_name'] 

            districtdata = list(District_master.objects.filter(id=data['district_id']).values())
                        
            for c in districtdata:
                districtname = c['district_name']

            talukdata = list(Taluk_master.objects.filter(id=data['taluk_id']).values())
                        
            for c in talukdata:
                talukname = c['taluk_name']
            
            userss = get_user_model().objects.create_user(email=data['email'],password=data['password'],mobile_number=data['mobile_number'],full_name=data['full_name'],state=statename,district=districtname,state_id=data['state_id'],district_id=data['district_id'],taluk=talukname,taluk_id=data['taluk_id'],role='user',role_id=4,otp=otp,otp_expiry=datetime.datetime.now() + datetime.timedelta(minutes = 10))
            userss.save()
            mydata = {'data':'User successfully created','code':status.HTTP_201_CREATED,'detail':'Success'}
        else:
            mydata = {'data':'user exists','code':status.HTTP_409_CONFLICT,'detail':'user already exists'}
        return Response(mydata)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get']
    def list(self, request,pk=None):
        if request.user.is_authenticated:
            users = request.user
            usersid = users.id
            User_info=list(get_user_model().objects.filter(id=usersid).values())
            prefix = 'DFO-'
            id = ''
            fullname = ''
            email = ''
            mobile = ''
            prophoto = ''
            state_id=''
            district_id=''
            state=''
            district=''
            taluk = ''
            taluk_id=''
            for x in User_info:
                fullname = x['full_name']
            for x in User_info:
                id = x['id']
            for x in User_info:
                email = x['email']
            for x in User_info:
                mobile = x['mobile_number']
            for x in User_info:
                state_id = x['state_id']
            for x in User_info:
                district_id = x['district_id']
            for x in User_info:
                state = x['state']
            for x in User_info:
                district= x['district']
            for x in User_info:
                taluk= x['taluk']
            for x in User_info:
                taluk_id= x['taluk_id']

            check = Form.objects.filter(createdby=usersid).exists()
            if check == True:
                usersform = list(Form.objects.filter(createdby=usersid).values())
                for x in usersform:
                    document= x['document_photo']
            else:
                document='Null'
                
            checking = get_user_model().objects.filter(id=usersid)
            serializer = Photoserializer(checking,many=True)
            pic = ''
            for x in serializer.data:
                pic = x['profile_photo']
            prefixid = str(prefix)+str(id)
            print(prefixid)
            datas = {'id':prefixid,'full_name':fullname,'email':email,'mobile_number':mobile,'profile_photo':pic,'document_photo':document,'district_id':district_id,'state_id':state_id,'district':district,'state':state,'taluk':taluk,'taluk_id':taluk_id}
            #serializer = ProfileSerializer(User_info,many=True)
            mydata = {'data':datas,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Otp_validateViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Otp_validateSerializer
    http_method_names = ['post',]
    def create(self,request):
        data = request.data
        mobile = data['mobile_number']
        rotp = data['otp']
        qs = list(get_user_model().objects.filter(mobile_number=mobile).values())
        sotp = ''
        exptime = ''
        for x in qs:
            sotp = x['otp']
        for x in qs:
            exptime = x['otp_expiry']
            
        nw = datetime.datetime.now().time()
        expriytime = exptime.time()
        if nw < expriytime:
            if sotp == rotp :
                validated = get_user_model().objects.filter(mobile_number=mobile).update(is_otpvalidated=True)
                mydata =  {'data':'Verified','code':status.HTTP_200_OK,'detail':'Sccuess'}
                return Response(mydata)
            else:
                mydata = {'data':'wrong otp','code':status.HTTP_400_BAD_REQUEST,'detail':'wrong otp'}
                return Response(mydata)
        else:
                mydata = {'data':'otp expired','code':status.HTTP_400_BAD_REQUEST,'detail':'wrong otp'}
                return Response(mydata)

class Check_verifiedViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Check_verifiedserializer
    http_method_names = ['get']

    def list(self,request):
        user = request.user
        if request.user.is_authenticated:
            usersid = user.id
            qs =  list(get_user_model().objects.filter(id=usersid).values())
            verify = ''
            payment =''
            form = ''
            paymentverify=''
            form_verify = ''
            state_id=''
            taluk_id = ''
            district_id=''
            for c in qs:
                verify = c['is_verified']

            for c in qs:
                payment = c['is_paymentdone']

            for c in qs:
                form = c['is_formupdated']

            for c in qs:
                otp = c['is_otpvalidated']

            for c in qs:
                paymentverify = c['payment_verified']
            for c in qs:
                form_verify = c['form_verified']

            for c in qs:
                state_id = c['state_id']
            for c in qs:
                district_id=c['district_id']
            for c in qs:
                taluk_id=c['taluk_id']
            

            datas = {'is_verified':verify,'is_paymentdone':payment,'is_formupdated':form,'is_otpvalidated':otp,'payment_verified':paymentverify,'form_verified':form_verify,'state_id':state_id,'district_id':district_id,'taluk_id':taluk_id}
            mydata = {'data':datas,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

from django.views.decorators.csrf import csrf_exempt,csrf_protect
import requests
import random

class Resend_otp(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = get_user_model().objects.all()
    serializer_class = Otp_ResendSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Resend_otp, self).dispatch(request, *args, **kwargs)

    def create(self,request):
        data = request.data
        mobile = data['mobile_number']
        check =get_user_model().objects.filter(mobile_number=mobile).exists()
        if check == True:
            otp = random.randint(1000,9999)
            statu = send_otp(mobile,otp)
            qs =  get_user_model().objects.filter(mobile_number=mobile).update(otp=otp,otp_expiry=datetime.datetime.now() + datetime.timedelta(minutes = 10))
            mydata = {'data':{'Success sent otp':otp},'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else: 
            mydata = {'data':'Mobile Number Not Found','code':status.HTTP_404_NOT_FOUND,'detail':'Failure'}
            return Response(mydata)

class GetPaymentviewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = GetPaymentSerializer
    http_method_names = ['get']
    def list(self, request):
        if request.user.is_authenticated:
            users = request.user
            usersid = users.id
            userstate = users.state_id
            User_info=Payment.objects.filter(state_id=userstate)
            serializer = PaymentSerializer(User_info,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})



class Formviewset(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    http_method_names = ['get','post','put']
    def list(self, request):
        if request.user.is_authenticated:
            users = request.user
            usersid = users.id
            User_info=Form.objects.filter(createdby=usersid)
            serializer = FormSerializer(User_info,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})
    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            users = request.user
            usersid = users.id
            name = users.full_name
            mobile = users.mobile_number
            email = users.email
            state_id = users.state_id
            district_id = users.district_id
            taluk_id = users.taluk_id
            taluk = users.taluk
            state = users.state
            district = users.district
            check = Form.objects.filter(createdby=usersid).exists()
            if check == False:
                userss = Form.objects.create(name=name,mobile=mobile,email=email,date_of_birth=data['date_of_birth'],aadhar_no=data['aadhar_no'],address=data['address'],qualification=data['qualification'],pan_number=data['pan_number'],csc_id=data['csc_id'],csc_id_number=data['csc_id_number'],bc_id=data['bc_id'],bc_id_number=data['bc_id_number'],csp_id=data['csp_id'],csp_id_number=data['csp_id_number'],pincode=data['pincode'],state=state,state_id=state_id,city=data['city'],taluk=taluk,district_id=district_id,district=district,taluk_id=taluk_id,terms_condition=data['terms_condition'],createdby=usersid)
                update =  get_user_model().objects.filter(id=usersid).update(pincode=data['pincode'],city=data['city'],taluk=data['taluk'],is_formupdated=True)
                mydata = {'data':'Form fill success','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else :
                userss = Form.objects.filter(createdby=usersid).update(name=name,mobile=mobile,email=email,date_of_birth=data['date_of_birth'],aadhar_no=data['aadhar_no'],address=data['address'],pan_number=data['pan_number'],csc_id=data['csc_id'],csc_id_number=data['csc_id_number'],bc_id=data['bc_id'],bc_id_number=data['bc_id_number'],csp_id=data['csp_id'],csp_id_number=data['csp_id_number'],pincode=data['pincode'],city=data['city'],terms_condition=data['terms_condition'],state=state,state_id=state_id,district=district,district_id=district_id,taluk_id=taluk_id)

                update =  get_user_model().objects.filter(id=usersid).update(pincode=data['pincode'],city=data['city'],is_formupdated=True)
                mydata = {'data':'Form Update success','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


class AttendenceviewSet(viewsets.ModelViewSet):
    queryset = Attendence.objects.all()
    serializer_class = AttendenceSerializer
    http_method_names = ['get','post']

    def list(self,request):
        if request.user.is_authenticated:
            users = request.user
            usersid = users.id
            User_info=Attendence.objects.filter(user_id=usersid)
            serializer = AttendenceSerializer(User_info,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            user = request.user
            usersid = user.id
            check = Attendence.objects.filter(date=data['date'],user_id=usersid).exists()
            if check == True:
                mydata = {'data':'Given date is already updated','code':status.HTTP_409_CONFLICT,'detail':'Failure'}
                return Response(mydata)
            else:
                create = Attendence.objects.create(date=data['date'],status=data['status'],user_id=usersid)
                mydata = {'data':'Successfully updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


class Checkattendenceview(viewsets.ModelViewSet):
    queryset = Attendence.objects.all()
    serializer_class = Checkattendence
    http_method_names = ['post',]

    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            users = request.user
            usersid = users.id
            check = Attendence.objects.filter(date=data['date'],user_id=usersid).exists()
            if check == False:
                qs = list(Sample.objects.filter(id=1).values())
                res = ''
                for x in qs:
                    res = x['is_boolean']
                mydata = {'data':res,'code':status.HTTP_404_NOT_FOUND,'detail':'Failure'}
                return Response(mydata)
            else:
                qs1 = list(Attendence.objects.filter(date=data['date'],user_id=usersid).values())
                res1 = ''
                for x in qs1:
                    res1 = x['status']
                mydata = {'data':res1,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)

        else:
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})



from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.parsers import FormParser, MultiPartParser


class Upload_screenshot(CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                      DestroyModelMixin, viewsets.GenericViewSet):
    http_method_names = ['post']
    queryset = get_user_model().objects.all()
    serializer_class = upload_screenshot
    parser_classes = (FormParser, MultiPartParser)

    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            user = request.user
            usersid = user.id
            mobile = user.mobile_number
            #update =  get_user_model().objects.filter(mobile_number=mobile).update(is_paymentdone=True)
            qs = get_user_model().objects.filter(mobile_number=mobile).update(payment_photo=data['payment_photo'])
            user.is_paymentdone = True
            user.payment_photo = data['payment_photo']
            user.save()
            image_url = user.profile_photo
            mydata = {'data':'Upload successful','code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


class Upload_document(CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                      DestroyModelMixin, viewsets.GenericViewSet):
    http_method_names = ['post']
    queryset = get_user_model().objects.all()
    serializer_class = upload_document
    parser_classes = (FormParser, MultiPartParser)

    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            user = request.user
            usersid = user.id
            mobile = user.mobile_number
            #update =  get_user_model().objects.filter(mobile_number=mobile).update(is_paymentdone=True)
            qs = get_user_model().objects.filter(mobile_number=mobile).update(document_photo=data['document_photo'])
            qs1 = Form.objects.filter(createdby=usersid).update(document_photo=data['document_photo'])
            user.document_photo = data['document_photo']
            user.save()
            image_url = user.document_photo
            mydata = {'data':'Upload successful','code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

from .utils import Util
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.urls import reverse

class Forgotpasswordview(viewsets.ModelViewSet):
    queryset =  get_user_model().objects.all()
    serializer_class = Forgotpasswordserilaizer
    http_method_names = ['post',]

    def create(self,request):
        data = request.data
        check =get_user_model().objects.filter(mobile_number=data['mobile_number']).exists()
        if check == True:
            qs = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
            email = ''
            for x in qs:
                email = x['email']

            user = get_user_model().objects.get(mobile_number=data['mobile_number'])
            token = PasswordResetTokenGenerator().make_token(user)
            update = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(email_token=token,otp_expiry=datetime.datetime.now() + datetime.timedelta(minutes = 10))
            absurl = 'http://dfo.hktech.in/password-reset.html?Mg=' + token
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl
            data = {'email_body': email_body, 'to_email': email,
                    'email_subject': 'Reset your passsword'}
            print(absurl)
            Util.send_email(data)
            mydata = {'data':'Mail sent success','code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'User Not Found','status':status.HTTP_404_NOT_FOUND,'detail': 'Failure , Login Falied'})


class Getallstate(viewsets.ModelViewSet):
    queryset = State_master.objects.all()
    serializer_class = Stateserializer
    http_method_names = ['get']
    def list(self,request):
        qs = State_master.objects.all()
        serializer = Stateserializer(qs,many=True)
        mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
        return Response(mydata)


class Getalldistrict(views.APIView):
    serializer_class = Districtserializer
    token_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        id = request.GET.get('id')
        check = State_master.objects.filter(id=id).exists()
        if check ==True:
            qs = District_master.objects.filter(state_id=id)
            serializer = Districtserializer(qs,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            mydata = {'data':'State not found','code':status.HTTP_404_NOT_FOUND,'detail':'Success'}
            return Response(mydata)

class Getalltaluk(views.APIView):
    serializer_class = TaluksSerializer
    token_param_config = openapi.Parameter(
        'state_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config1 = openapi.Parameter(
        'district_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config,token_param_config1])
    def get(self,request):
        state_id = request.GET.get('state_id')
        district_id =  request.GET.get('district_id')
        check = Taluk_master.objects.filter(state_id=state_id,district_id=district_id).exists()
        if check ==True:
            qs = Taluk_master.objects.filter(state_id=state_id,district_id=district_id)
            serializer = TaluksSerializer(qs,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            mydata = {'data':'State not found','code':status.HTTP_404_NOT_FOUND,'detail':'Success'}
            return Response(mydata)

class Popupview(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Popupserializer
    http_method_names = ['post']
    def create(self,request):
        if request.user.is_authenticated:
            users = request.user
            data= request.data
            usersid=users.id
            statedata = list(State_master.objects.filter(id=data['state_id']).values())
            statename = ''
            districtname = ''
            talukname = ''

            for c in statedata:
                statename = c['state_name']

            districtdata = list(District_master.objects.filter(id=data['district_id']).values())
                        
            for c in districtdata:
                districtname = c['district_name']

            talukdata = list(Taluk_master.objects.filter(id=data['taluk_id']).values())
                        
            for c in talukdata:
                talukname = c['taluk_name']
                
            qs = get_user_model().objects.filter(id=usersid).update(state_id=data['state_id'],district_id=data['district_id'],state=statename,district=districtname,taluk=talukname,taluk_id=data['taluk_id'])
            mydata = {'data':'Update Success','code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'login again','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


