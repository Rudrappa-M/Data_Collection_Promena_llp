from django.shortcuts import render
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.translation import activate
from rest_framework.response import Response
from rest_framework import status,viewsets, views,generics,status
from Models.models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
import coreapi
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
import random
from .tests import *
import pandas as pd
# Create your views here.

from django.contrib.auth.mixins import UserPassesTestMixin

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class CreateUsers(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['post']
    def create(self,request):
        data = request.data
        mobile_number=data['mobile_number']
        check =get_user_model().objects.filter(mobile_number=mobile_number).exists()
        if check == False:
            userss = get_user_model().objects.create_user(email=data['email'],password=data['password'],mobile_number=data['mobile_number'],role=data['role'],is_staff=True,otp=1234)
            userss.save()
            mydata = {'data':'User successfully created','code':status.HTTP_201_CREATED,'detail':'Success'}
        else:
            mydata = {'data':'User exists','code':status.HTTP_409_CONFLICT,'detail':'user already exists'}
        return Response(mydata)

class Profile(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Profileserializer
    http_method_names = ['get']
    def list(self, request,pk=None):
        if request.user.is_authenticated:
            users = request.user
            usersid = users.id
            User_info=get_user_model().objects.filter(id=usersid)
            serializer = Profileserializer(User_info,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Updatepaymentdetials(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = Updatepaymentdetials
    http_method_names = ['put']
    def update(self, request):
        if request.user.is_authenticated:
            users = request.user
            data= request.data
            usersid = users.id
            roleid = users.role_id
            userstate = users.state
            if roleid is None:
                User_info=Payment.objects.filter(state=userstate).update(phone_pe_number=data['phone_pe_number'],google_pay_number=data['google_pay_number'],upi_id=data['upi_id'],amount=data['amount'])
                mydata = {'data':'Successfully Updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            elif roleid == 1:
                User_info=Payment.objects.filter(state=userstate).update(phone_pe_number=data['phone_pe_number'],google_pay_number=data['google_pay_number'],upi_id=data['upi_id'],amount=data['amount'])
                mydata = {'data':'Successfully Updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class VerifyuserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Verifyuserserializer
    http_method_names = ['post',]
    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            user = request.user
            roleid = user.role_id
            if roleid is None:
                query = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(is_verified=data['is_verified'],approved_by=user.id)
                mydata = {'data':'updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            elif roleid == 1:
                query = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(is_verified=data['is_verified'],approved_by=user.id)
                mydata = {'data':'updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class PaymentverifyuserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Paymentverifyuserserializer
    http_method_names = ['post',]
    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            user = request.user
            roleid = user.role_id
            if roleid is None:
                query = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(payment_verified=data['payment_verified'],approved_by=user.id)
                mydata = {'data':'updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            elif roleid == 1:
                query = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(payment_verified=data['payment_verified'],approved_by=user.id)
                mydata = {'data':'updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class FormverifyuserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Formverifyuserserializer
    http_method_names = ['post',]
    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            user = request.user
            roleid = user.role_id
            if roleid is None:
                query = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(form_verified=data['form_verified'])
                update = Form.objects.filter(mobile=data['mobile_number']).update(form_verified=data['form_verified'])
                mydata = {'data':'updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            elif roleid == 1:
                query = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(form_verified=data['form_verified'])
                update = Form.objects.filter(mobile=data['mobile_number']).update(form_verified=data['form_verified'])
                mydata = {'data':'updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})



class Getuserstatus(views.APIView):
    serializer_class = Userstatusserializer
    token_param_config = openapi.Parameter(
        'mobile_number', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        if request.user.is_authenticated:
            data = request.data
            mobile_number=request.GET.get('mobile_number')
            user = request.user
            query = get_user_model().objects.filter(mobile_number=mobile_number)
            serializer = Userstatusserializer(query,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Getallforms(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormsSerializer
    http_method_names = ['get']
    token_param_config1 = openapi.Parameter(
        'page', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config2 = openapi.Parameter(
        'index', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config3 = openapi.Parameter(
        'search', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config1,token_param_config2,token_param_config3])
    def list(self,request):
        if request.user.is_authenticated:
            user = request.user
            role_id = user.role_id
            if role_id is None:
                search = request.GET.get('search')
                if search is None:
                    query = Form.objects.exclude(mobile='9876543210',createdby=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = FormsSerializer(page_obj,many=True)
                    count = Form.objects.exclude(mobile='9876543210',createdby=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
                else:
                    query = Form.objects.filter(Q(name__contains=search)|Q(mobile__contains=search)|Q(email__contains=search)).exclude(mobile='9876543210',createdby=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = FormsSerializer(page_obj,many=True)
                    count = Form.objects.filter(Q(name__contains=search)|Q(mobile__contains=search)|Q(email__contains=search)).exclude(mobile='9876543210',createdby=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
            elif role_id == 3:
                search = request.GET.get('search')
                if search is None:
                    qs = get_user_model().objects.filter(talukhead_id=user.id).values_list('id', flat=True)
                    query = Form.objects.filter(createdby__in=qs).exclude(mobile='9876543210',createdby=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = FormsSerializer(page_obj,many=True)
                    count= Form.objects.filter(createdby__in=qs).exclude(mobile='9876543210',createdby=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
                else:
                    qs = get_user_model().objects.filter(talukhead_id=user.id).values_list('id', flat=True)
                    query = Form.objects.filter(Q(name__contains=search)|Q(mobile__contains=search)|Q(email__contains=search)&Q(createdby__in=qs)).exclude(mobile='9876543210',createdby=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = FormsSerializer(page_obj,many=True)
                    count =  Form.objects.filter(Q(name__contains=search)|Q(mobile__contains=search)|Q(email__contains=search)&Q(createdby__in=qs)).exclude(mobile='9876543210',createdby=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
            elif role_id == 2:
                search = request.GET.get('search')
                if search is None:
                    qs = get_user_model().objects.filter(assigned_districtid=user.assigned_districtid,role_id=3).values_list('id',flat=True)
                    query =  Form.objects.filter(createdby__in=qs).exclude(mobile='9876543210',createdby=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = FormsSerializer(page_obj,many=True)
                    count = Form.objects.filter(createdby__in=qs).exclude(mobile='9876543210',createdby=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
                else:
                    qs = get_user_model().objects.filter(assigned_districtid=user.assigned_districtid,role_id=3).values_list('id',flat=True)
                    query = Form.objects.filter(Q(name__contains=search)|Q(mobile__contains=search)|Q(email__contains=search)&Q(createdby__in=qs)).exclude(mobile='9876543210',createdby=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = FormsSerializer(page_obj,many=True)
                    count = Form.objects.filter(Q(name__contains=search)|Q(mobile__contains=search)|Q(email__contains=search)&Q(createdby__in=qs)).exclude(mobile='9876543210',createdby=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
            elif role_id == 1:
                search = request.GET.get('search')
                if search is None:
                    qs = get_user_model().objects.filter(assigned_stateid=user.assigned_stateid,state_id=user.assigned_stateid).values_list('id',flat=True)
                    query = Form.objects.filter(createdby__in=qs).exclude(mobile='9876543210',createdby=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = FormsSerializer(page_obj,many=True)
                    count = Form.objects.filter(createdby__in=qs).exclude(mobile='9876543210',createdby=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
                else:
                    qs = get_user_model().objects.filter(assigned_stateid=user.assigned_stateid,state_id=user.assigned_stateid).values_list('id',flat=True)
                    query = Form.objects.filter(Q(name__contains=search)|Q(mobile__contains=search)|Q(email__contains=search)&Q(createdby__in=qs)).exclude(mobile='9876543210',createdby=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = FormsSerializer(page_obj,many=True)
                    count = Form.objects.filter(Q(name__contains=search)|Q(mobile__contains=search)|Q(email__contains=search)&Q(createdby__in=qs)).exclude(mobile='9876543210',createdby=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
        return Response(mydata)

class Get_allusers(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = get_user_model().objects.all()
    serializer_class = Getallusers
    token_param_config1 = openapi.Parameter(
        'page', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config2 = openapi.Parameter(
        'index', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config3 = openapi.Parameter(
        'search', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config1,token_param_config2,token_param_config3])
    def list(self,request):
        if request.user.is_authenticated:
            user = request.user
            role_id = user.role_id
            if role_id is None:
                search = request.GET.get('search')
                if search is None:
                    query = get_user_model().objects.exclude(mobile_number='9876543210').distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = Getallusers(page_obj,many=True)
                    count = get_user_model().objects.exclude(mobile_number='9876543210').count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
                else:
                    query = get_user_model().objects.filter(Q(full_name__contains=search)|Q(email__contains=search)|Q(mobile_number__contains=search)).exclude(mobile_number='9876543210').distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = Getallusers(page_obj,many=True)
                    count = get_user_model().objects.filter(Q(full_name__contains=search)|Q(email__contains=search)|Q(mobile_number__contains=search)).exclude(mobile_number='9876543210').count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
            elif role_id == 3:
                search = request.GET.get('search')
                if search is None:
                    query = get_user_model().objects.filter(talukhead_id=user.id).exclude(mobile_number='9876543210',id=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = Getallusers(page_obj,many=True)
                    count = get_user_model().objects.filter(talukhead_id=user.id).exclude(mobile_number='9876543210',id=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
                else:
                    query = get_user_model().objects.filter(Q(full_name__contains=search)|Q(email__contains=search)|Q(mobile_number__contains=search)&Q(talukhead_id=user.id)).exclude(mobile_number='9876543210',id=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = Getallusers(page_obj,many=True)
                    count = get_user_model().objects.filter(Q(full_name__contains=search)|Q(email__contains=search)|Q(mobile_number__contains=search)&Q(talukhead_id=user.id)).exclude(mobile_number='9876543210',id=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
            elif role_id == 2:
                search = request.GET.get('search')
                if search is None:
                    query = get_user_model().objects.filter(assigned_districtid=user.assigned_districtid,role_id=3).exclude(mobile_number='9876543210',id=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = Getallusers(page_obj,many=True)
                    count = get_user_model().objects.filter(assigned_districtid=user.assigned_districtid,role_id=3).exclude(mobile_number='9876543210',id=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
                else:
                    query = get_user_model().objects.filter(Q(full_name__contains=search)|Q(email__contains=search)|Q(mobile_number__contains=search)&Q(assigned_districtid=user.assigned_districtid)&Q(role_id=3)).exclude(mobile_number='9876543210',id=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = Getallusers(page_obj,many=True)
                    count = get_user_model().objects.filter(Q(full_name__contains=search)|Q(email__contains=search)|Q(mobile_number__contains=search)&Q(assigned_districtid=user.assigned_districtid)&Q(role_id=3)).exclude(mobile_number='9876543210',id=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
            elif role_id == 1:
                search = request.GET.get('search')
                if search is None:
                    query = get_user_model().objects.filter(assigned_stateid=user.assigned_stateid,state_id=user.assigned_stateid).exclude(mobile_number='9876543210',id=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = Getallusers(page_obj,many=True)
                    count = get_user_model().objects.filter(assigned_stateid=user.assigned_stateid,state_id=user.assigned_stateid).exclude(mobile_number='9876543210',id=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
                else:
                    role_id_list = [2,3]
                    query = get_user_model().objects.filter(Q(full_name__contains=search)|Q(email__contains=search)|Q(mobile_number__contains=search)&Q(assigned_stateid=user.assigned_stateid,state_id=user.assigned_stateid)).exclude(mobile_number='9876543210',id=user.id).distinct()
                    index = request.GET.get('index')
                    paginator = Paginator(query, index)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    serializer = Getallusers(page_obj,many=True)
                    count = get_user_model().objects.filter(Q(full_name__contains=search)|Q(email__contains=search)|Q(mobile_number__contains=search)&Q(assigned_stateid=user.assigned_stateid,state_id=user.assigned_stateid)).exclude(mobile_number='9876543210',id=user.id).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success','page':page_number,'index':index,'total_count':count}
                    return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


class GetallWorkers(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = get_user_model().objects.all()
    serializer_class = GetallWorkerserializer

    def list(self,request):
        if request.user.is_authenticated:
            qs = get_user_model().objects.filter(is_superuser=False).exclude(role='user')
            serializer = GetallWorkerserializer(qs,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.parsers import FormParser, MultiPartParser



class Upload_profilephoto(CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                      DestroyModelMixin, viewsets.GenericViewSet):
    http_method_names = ['post']
    queryset = get_user_model().objects.all()
    serializer_class = Upload_profilephoto
    parser_classes = (FormParser, MultiPartParser)

    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            user = request.user
            mobile = user.mobile_number
            qs = get_user_model().objects.filter(id=user.id).update(profile_photo=data['profile_photo'])
            user.profile_photo = data['profile_photo']
            user.save()
            image_url = user.profile_photo
            mydata = {'data':'Upload successful','code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Upload_QRcode(CreateModelMixin, ListModelMixin, RetrieveModelMixin,
                      DestroyModelMixin, viewsets.GenericViewSet):
    http_method_names = ['post']
    queryset = get_user_model().objects.all()
    serializer_class = Upload_Qrphoto
    parser_classes = (FormParser, MultiPartParser)

    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            users = request.user
            roleid = users.role_id
            if roleid is None:
                userstate = data['state_id']
                qs = Payment.objects.filter(state_id=userstate).update(qr_code=data['qr_code'])
                payment = Payment(qr_code=data['qr_code'])
                payment.save()
                image_url = payment.qr_code
                mydata = {'data':'Upload successful','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                    mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                    return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Requestupdateform(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = RequestupdateformSerializer
    http_method_names = ['post']
    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            users = request.user
            roleid = users.role_id
            if roleid is None:
                qs = get_user_model().objects.filter(mobile_number=data['mobile']).update(is_formupdated=False,form_verified=False)
                qs1 = Form.objects.filter(mobile=data['mobile']).update(form_verified=False)
                mydata = {'data':'update requested success','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)

            elif roleid == 1:
                qs = get_user_model().objects.filter(mobile_number=data['mobile']).update(is_formupdated=False,form_verified=False)
                qs1 = Form.objects.filter(mobile=data['mobile']).update(form_verified=False)
                mydata = {'data':'update requested success','code':status.HTTP_200_OK,'detail':'Success'}
                
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})
                

class Postpayment(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PostPaymentSerializer
    http_method_names = ['post']
   
    def create(self,request):
        if request.user.is_authenticated:
            data = request.data
            users = request.user
            userstate = users.state
            roleid = users.role_id
            stateid = data['state_id']
            check = Payment.objects.filter(state_id=data['state_id']).exists()
            if check == False:
                if roleid is None:
                    create = Payment.objects.create(phone_pe_number=data['phone_pe_number'],google_pay_number=data['google_pay_number'],upi_id=data['upi_id'],state_id=data['state_id'],amount=data['amount'])
                    mydata = {'data':'Successfully updated','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                else:
                    mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                    return Response(mydata)
            else:
                if roleid is None:
                    User_info=Payment.objects.filter(state_id=stateid).update(phone_pe_number=data['phone_pe_number'],google_pay_number=data['google_pay_number'],upi_id=data['upi_id'],amount=data['amount'])
                    mydata = {'data':'Successfully Updated','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                else:
                    mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                    return Response(mydata)       
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Paymentdetailsallstates(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['get']
    token_param_config3 = openapi.Parameter(
        'state_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config3])
    def list(self,request):

        if request.user.is_authenticated:
            users  = request.user
            roleid = users.role_id
            userstate = users.state_id
            stateid = request.GET.get('state_id')
            if roleid is None:
                qs = Payment.objects.filter(state_id=stateid)
                serializer = PaymentSerializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})
class Paymentdetails(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['get']

    def list(self,request):

        if request.user.is_authenticated:
            users  = request.user
            userstate = users.state_id
            roleid = users.role_id
            if roleid ==1:
                qs = Payment.objects.filter(state_id=users.assigned_stateid)
                serializer = PaymentSerializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            elif roleid ==2:
                qs1 = list(District_master.objects.filter(id=users.assigned_districtid).values())
                stateid=''
                for q in qs1:
                    stateid = q['state_id']
                qs = Payment.objects.filter(state_id=stateid)
                serializer = PaymentSerializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            elif roleid ==3:
                qs1 = list(Taluk_master.objects.filter(id=users.assigned_talukid).values())
                stateid=''
                for q in qs1:
                    stateid = q['state_id']
                qs = Payment.objects.filter(state_id=stateid)
                serializer = PaymentSerializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            else:
                qs = Payment.objects.filter(state_id=users.state_id)
                serializer = PaymentSerializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Formapproveviewset(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = Formapproveserializer
    http_method_names = ['post']

    def create(self, request):
        if request.user.is_authenticated:
            data = request.data
            user = request.user
            roleid = user.role_id
            if roleid is None:
                qs = Form.objects.filter(mobile=data['mobile']).update(form_verified=data['form_verified'])
                qs1 = get_user_model().objects.filter(mobile=data['mobile']).update(form_verified=data['form_verified'])
                mydata = {'data':'Successfully updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            elif roleid == 1:
                qs = Form.objects.filter(mobile=data['mobile']).update(form_verified=data['form_verified'])
                qs1 = get_user_model().objects.filter(mobile=data['mobile']).update(form_verified=data['form_verified'])
                mydata = {'data':'Successfully updated','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else :
            raise AuthenticationFailed({'data':'Failure','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Getpaymentdetails(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = get_user_model().objects.all()
    serializer_class = Getpaymentdetailserializer

    def list(self,request):

        if request.user.is_authenticated:
            users = request.user
            userstate = users.state
            roleid = user.role_id
            if roleid is None:
                qs = get_user_model().objects.filter(is_paymentdone=True)
                serializer = Getpaymentdetailserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            elif roleid == 1:
                qs = get_user_model().objects.filter(is_paymentdone=True,state=userstate)
                serializer = Getpaymentdetailserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    #permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if request.user.is_authenticated:

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"detail": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'detail': 'success',
                    'code': status.HTTP_200_OK,
                    'data': ['Password updated successfully']
                }

                return Response(response)
        else :
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Rolesview(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = Roleserializer
    http_method_names = ['get']

    def list(self,request):

        if request.user.is_authenticated:
            qs = Role.objects.all()
            serializer = Roleserializer(qs,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


class DeleteRole(views.APIView):
    serializer_class = DeleteRoleserializer
    token_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def delete(self,request):
        id = request.GET.get('id')
        if request.user.is_authenticated:
            check = Role.objects.filter(id=id).exists()
            if check ==True:
                if id not in ('1','2','3','4'):
                    qs = Role.objects.filter(id=id).delete()
                    mydata = {'data':'Deleted','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                else :
                     mydata = {'data':'Cannot Delete this role','code':status.HTTP_400_BAD_REQUEST,'detail':'Failure'}
                     return Response(mydata)
            else:
                mydata = {'data':'Role not found','code':status.HTTP_404_NOT_FOUND,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class CreateRolesview(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = CreateRoleserializer
    http_method_names = ['post']
    def create(self,request):

        if request.user.is_authenticated:
            data = request.data
            check = Role.objects.filter(rolename = data['rolename']).exists()
            if check == False:
                qs = Role.objects.create(rolename = data['rolename'])
                mydata = {'data':'Role Added','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'Role Already exists','code':status.HTTP_409_CONFLICT,'detail':'Failure'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class AssignRoleview(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = AssignRoleserializer
    http_method_names = ['post']
    def create(self,request):

        if request.user.is_authenticated:
            data = request.data
            users = request.user
            usersid = users.id
            roleid = users.role_id
            datas = list(Role.objects.filter(id=data['role_id']).values())
            rolename = ''
            asignroleid = data['role_id']
            for x in datas :
                rolename = x['rolename']
            if roleid is None:
                if asignroleid == 1:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['assigned_stateid']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],role=rolename,assigned_stateid=data['assigned_stateid'],approved_by=usersid)
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                elif asignroleid ==2:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['assigned_districtid']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],assigned_stateid=data['assigned_stateid'],assigned_districtid=data['assigned_districtid'],role=rolename,approved_by=usersid)
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                elif asignroleid ==3:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['assigned_talukid']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],assigned_stateid=data['assigned_stateid'],assigned_districtid=data['assigned_districtid'],assigned_talukid=data['assigned_talukid'],role=rolename,approved_by=usersid)
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                elif asignroleid ==5:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['role_id']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],role=rolename,assigned_stateid=data['assigned_stateid'],assigned_districtid=data['assigned_districtid'],approved_by=usersid)
                    qs1 = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(statehead_id=data['statehead_id'],districthead_id=data['districthead_id'],talukhead_id=data['talukhead_id'])
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                else:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['role_id']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],role=rolename,assigned_stateid=data['assigned_stateid'],assigned_districtid=data['assigned_districtid'],approved_by=usersid)
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
            elif roleid == 1:
                if asignroleid == 1:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['assigned_stateid']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],role=rolename,assigned_stateid=data['assigned_stateid'],approved_by=usersid)
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                elif asignroleid ==2:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['assigned_districtid']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],role=rolename,assigned_stateid=data['assigned_stateid'],assigned_districtid=data['assigned_districtid'],approved_by=usersid)
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                elif asignroleid ==3:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['assigned_talukid']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],role=rolename,assigned_stateid=data['assigned_stateid'],assigned_districtid=data['assigned_districtid'],assigned_talukid=data['assigned_talukid'],approved_by=usersid)
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                elif asignroleid ==4:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['role_id']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],role=rolename,talukhead_id=data['talukhead_id'],statehead_id=data['statehead_id'],districthead_id=data['districthead_id'],approved_by=usersid)
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                else:
                    userinfo = list(get_user_model().objects.filter(mobile_number=data['mobile_number']).values())
                    for u in userinfo:
                        userid = u['id']
                    designationid = Designationid(userid,data['role_id']) 
                    qs = get_user_model().objects.filter(mobile_number=data['mobile_number']).update(designation_id=designationid,role_id=data['role_id'],role=rolename,assigned_stateid=data['assigned_stateid'],assigned_districtid=data['assigned_districtid'],approved_by=usersid)
                    mydata = {'data':'Role Updated success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'Login again','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})



class Createstate(viewsets.ModelViewSet):
    queryset = State_master.objects.all()
    serializer_class = Createstateserializer
    http_method_names = ['post']
    def create(self,request):

        if request.user.is_authenticated:
            data = request.data
            check = State_master.objects.filter(state_name = data['state_name']).exists()
            if check == False:
                qs = State_master.objects.create(state_name = data['state_name'])
                mydata = {'data':'State Added','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'State Already exists','code':status.HTTP_409_CONFLICT,'detail':'Failure'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'login again','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Deletestate(views.APIView):
    serializer_class = Deletestateserializer
    token_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def delete(self,request):
        id = request.GET.get('id')
        if request.user.is_authenticated:
            check = State_master.objects.filter(id=id).exists()
            if check ==True:
                qs = State_master.objects.filter(id=id).delete()
                mydata = {'data':'Deleted','code':status.HTTP_200_OK,'detail':'Success'}
            else:
                mydata = {'data':'State not found','code':status.HTTP_404_NOT_FOUND,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'Login again','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


class GetFormbyid(views.APIView):
    serializer_class = FormsSerializer
    token_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        id = request.GET.get('id')
        if request.user.is_authenticated:
            qs = Form.objects.filter(id=id)
            serializer = FormsSerializer(qs,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Getallstatehead(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Getallstateheadserializer
    http_method_names = ['get']
    token_param_config = openapi.Parameter(
        'state_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def list(self,request):
        state_id = request.GET.get('state_id')
        if request.user.is_authenticated:
            user = request.user
            usersrole = user.role_id
            if usersrole is None:
                qs = get_user_model().objects.filter(Q(role_id=1)&Q(assigned_stateid=state_id))
                serializer = Getallstateheadserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            elif usersrole == 1:
                qs = get_user_model().objects.filter(Q(role_id=1)&Q(assigned_stateid=state_id)|Q(statehead_id=user.id))
                serializer = Getallstateheadserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})
class Getalltalukhead(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Getallstateheadserializer
    http_method_names = ['get']

    token_param_config1 = openapi.Parameter(
        'state_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config2 = openapi.Parameter(
        'district_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config3 = openapi.Parameter(
        'taluk_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config1,token_param_config2,token_param_config3])
    def list(self,request):
        state_id = request.GET.get('state_id')
        district_id = request.GET.get('district_id')
        taluk_id = request.GET.get('taluk_id')
        if request.user.is_authenticated:
            user = request.user
            usersrole = user.role_id
            if usersrole is None:
                qs = get_user_model().objects.filter(Q(role_id=3)&Q(assigned_talukid=taluk_id))
                serializer = Getallstateheadserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            elif usersrole == 3:
                qs = get_user_model().objects.filter(Q(role_id=3)&Q(assigned_talukid=user.assigned_talukid)|Q(talukhead_id=user.id))
                serializer = Getallstateheadserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
            
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Getalldistricthead(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = Getallstateheadserializer
    http_method_names = ['get']
    token_param_config1 = openapi.Parameter(
        'state_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config2 = openapi.Parameter(
        'district_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config1,token_param_config2])
    def list(self,request):
        state_id = request.GET.get('state_id')
        district_id = request.GET.get('district_id')
        if request.user.is_authenticated:
            user = request.user
            usersrole = user.role_id
            if usersrole is None:
                qs = get_user_model().objects.filter(Q(role_id=2)&Q(assigned_districtid=district_id))
                serializer = Getallstateheadserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            elif usersrole == 2:
                qs = get_user_model().objects.filter(Q(role_id=2)&Q(assigned_districtid=district_id)|Q(districthead_id=user.id))
                serializer = Getallstateheadserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'UNAUTHORIZED','code':status.HTTP_401_UNAUTHORIZED,'detail':'Failure'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Getallstates(viewsets.ModelViewSet):
    queryset = State_master.objects.all()
    serializer_class = Createstateserializer
    http_method_names = ['get']
    def list(self,request):
        if request.user.is_authenticated:
            qs = State_master.objects.all()
            serializer = Createstateserializer(qs,many=True)
            mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'login again','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})

class Getalldistricts(views.APIView):
    serializer_class = Districtserializer
    token_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        id = request.GET.get('id')
        if request.user.is_authenticated:
            check = State_master.objects.filter(id=id).exists()
            if check ==True:
                qs = District_master.objects.filter(state_id=id)
                serializer = Districtserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
            else:
                mydata = {'data':'State not found','code':status.HTTP_404_NOT_FOUND,'detail':'Success'}
            return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'Login again','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


class Getalltaluks(views.APIView):
    serializer_class = Talukserializer
    token_param_config = openapi.Parameter(
        'state_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config1 = openapi.Parameter(
        'district_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config,token_param_config1])
    def get(self,request):
        state_id = request.GET.get('state_id')
        district_id =  request.GET.get('district_id')
        if request.user.is_authenticated:
            check = Taluk_master.objects.filter(state_id=state_id,district_id=district_id).exists()
            if check ==True:
                qs = Taluk_master.objects.filter(state_id=state_id,district_id=district_id)
                serializer = Talukserializer(qs,many=True)
                mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            else:
                mydata = {'data':'State not found','code':status.HTTP_404_NOT_FOUND,'detail':'Success'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'Login again','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


from .utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import datetime

class Forgotpasswordviews(viewsets.ModelViewSet):
    queryset =  get_user_model().objects.all()
    serializer_class = Forgotpasswordserilaizers
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
            print(token)
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



class Password_reset(views.APIView):
    serializer_class = passwordresetserializer
    token_param_config1 = openapi.Parameter(
        'password', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    token_param_config2 = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config1,token_param_config2])
    def post(self,request):
        token = request.GET.get('token')
        password = request.GET.get('password')
        users = list(get_user_model().objects.filter(email_token=token).values())
        uid = ''
        exptime = ''
        for u in users:
            uid = u['id']
        for u in users:
            exptime = u['otp_expiry']

        nw = datetime.datetime.now().time()
        expriytime = exptime.time()
        if nw < expriytime:
            try:
                user = get_user_model().objects.get(id=uid)
                user.set_password(password)
                user.save()
                datas = [password,token]
                mydata = {'data':'Password change success','code':status.HTTP_200_OK,'detail':'Success'}
                return Response(mydata)
            except Exception as e:
                raise AuthenticationFailed({'data':'User Not Found','status':status.HTTP_404_NOT_FOUND,'detail': 'Failure , Login Falied'})
        else:
                mydata = {'data':'wrong token','code':status.HTTP_400_BAD_REQUEST,'detail':'wrong otp'}
                return Response(mydata)


class Getallattendance(views.APIView):
    serializer_class = Getallattendanceserilaizers
    token_param_config = openapi.Parameter(
        'start_date', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    token_param_config1 = openapi.Parameter(
        'end_date', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    token_param_config2 = openapi.Parameter(
        'user_id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    token_param_config3 = openapi.Parameter(
        'page', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)
    token_param_config4 = openapi.Parameter(
        'index', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[token_param_config,token_param_config1,token_param_config2,token_param_config3,token_param_config4])
    def get(self,request):
        data = request.data
        start = request.GET.get('start_date')
        end = request.GET.get('end_date')
        usersid = request.GET.get('user_id')
        page = request.GET.get('page')
        index = request.GET.get('index')
        user = request.user
        if request.user.is_authenticated:
            if user.role_id is None:
                today = datetime.datetime.now().date()
                end = datetime.datetime.strptime(str(end), '%Y-%m-%d').date()
                if end < today:
                    daterange = pd.bdate_range(start=start,end=end)
                    qs = list(Attendence.objects.filter(date__range=[start,end],user_id=usersid).values())
                    datelist = []
                    for q in qs:
                        datelist.append(q['date'])
                    for d in daterange:
                        if d not in datelist:
                        
                            update = Attendence.objects.create(user_id=usersid,date=d,status=False)
                
                    qs1 = Attendence.objects.filter(date__range=[start,end],user_id=usersid)
                    paginator = Paginator(qs1, index)
                    page_obj = paginator.get_page(page)
                    serializer = Getallattendanceserilaizers(page_obj,many=True)
                    qs2 = Attendence.objects.filter(date__range=[start,end],user_id=usersid).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'page':page,'index':index,'total_count':qs2}
                    return Response(mydata)
                else:
                    daterange = pd.bdate_range(start=start,end=today)
                    qs = list(Attendence.objects.filter(date__range=[start,today],user_id=usersid).values())
                    datelist = []
                    for q in qs:
                        datelist.append(q['date'])
                    for d in daterange:
                        if d not in datelist:
                        
                            update = Attendence.objects.create(user_id=usersid,date=d,status=False)
                
                    qs1 = Attendence.objects.filter(date__range=[start,today],user_id=usersid)
                    paginator = Paginator(qs1, index)
                    page_obj = paginator.get_page(page)
                    serializer = Getallattendanceserilaizers(page_obj,many=True)
                    qs2 = Attendence.objects.filter(date__range=[start,today],user_id=usersid).count()
                    mydata = {'data':serializer.data,'code':status.HTTP_200_OK,'page':page,'index':index,'total_count':qs2}
                    return Response(mydata)
            else:
                mydata = {'data':'Unauthorized','code':status.HTTP_400_BAD_REQUEST,'detail':'Failure'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'Login again','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})


class Deleteform(views.APIView):
    serializer_class = Deleteformserilaizers
    token_param_config = openapi.Parameter(
        'mobile', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def delete(self,request):
        mobile = request.GET.get('mobile')
        user = request.user
        if request.user.is_authenticated:
            if user.role_id is None:
                check = Form.objects.filter(mobile=mobile).exists()
                if check == True:
                    update1 = Form.objects.filter(mobile=mobile).delete()
                    update2 = get_user_model().objects.filter(mobile_number=mobile).update(is_formupdated=False,form_verified=False)
                    mydata = {'data':'Form deleted success','code':status.HTTP_200_OK,'detail':'Success'}
                    return Response(mydata)
                else:
                    mydata = {'data':'Failure','code':status.HTTP_404_NOT_FOUND,'detail':'Failure'}
                    return Response(mydata)
            else:
                mydata = {'data':'Unauthorized','code':status.HTTP_400_BAD_REQUEST,'detail':'Failure'}
                return Response(mydata)
        else:
            raise AuthenticationFailed({'data':'Login again','status':status.HTTP_401_UNAUTHORIZED,'detail': 'Failure , Login Falied'})
 
