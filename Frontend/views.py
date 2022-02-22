from django.shortcuts import render
from django.shortcuts import render,redirect
# Create your views here.


def index(request):
    return render(request,'login.html')

def all_user(request):
    return render(request,'all_user.html')

def change_pasword(request):
    return render(request,'change_pasword.html')

def password_reset(request):
    return render(request,'password-reset.html')

def forget_password(request):
    return render(request,'forget_password.html')


def payment(request):
    return render(request,'payment.html')

def profile(request):
    return render(request,'profile.html')


def request(request):
    return render(request,'request.html')


def Roles(request):
    return render(request,'Roles.html')


def UserForms(request):
    return render(request,'UserForms.html')

def Attendance(request):
    return render (request,'Attendance.html')

def UserViewDetails(request):
    return render(request,'UserViewDetails.html')

def states(request):
    return render(request,'States.html')

def districts(request):
    return render(request,'Districts.html')

def subdistricts(request):
    return render(request,'SubDistricts.html')
def statehead(request):
    return render(request,'StateHead.html')
def districthead(request):
    return render(request,'DistrictHead.html')
def talukhead(request):
    return render(request,'SubDistrictHead.html')

def Userattendance(request):
    return render(request,'UserViewAttendance.html')
