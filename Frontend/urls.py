from django.urls import path
from .views import *


urlpatterns = [
    path('',index,name='main'),
    path('login.html',index,name='main'),
    path('all_user.html',all_user,name='all_user'),
    path('change_pasword.html',change_pasword,name='change_pasword'),
    path('forget_password.html',forget_password,name='forget_password'),
    path('payment.html',payment,name='payment'),
    path('profile.html',profile,name='profile'),
    path('request.html',request,name='request'),
    path('password-reset.html',password_reset,name='request'),
    path('Roles.html',Roles,name='Roles'),
    path('states.html',states,name='states'),
    path('Districts.html',districts,name='districts'),
    path('SubDistricts.html',subdistricts,name='subdistricts'),
    path('StateHead.html',statehead,name='states'),
    path('DistrictHead.html',districthead,name='districts'),
    path('SubDistrictHead.html',talukhead,name='subdistricts'),
    path('UserForms.html',UserForms,name='UserForms'),
    path('UserViewDetails.html',UserViewDetails,name='UserViewDetails'),
    path('Attendance.html',Attendance,name='Attendance'),
    path('UserViewAttendance.html',Userattendance,name='Attendance'),


]
