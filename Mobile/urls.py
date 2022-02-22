from django.urls import path,include
from .views import *
from Admin.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('Login/',LoginAPIView.as_view() ),
    path('Signup/',Signupviewset.as_view({'post': 'create',}) ),
    path('Otpvalidate/',Otp_validateViewSet.as_view({'post':'create'})),
    path('Resendotp/',Resend_otp.as_view({'post':'create'})),
    path('Checkverification/',Check_verifiedViewSet.as_view({'get':'list'})),
    path('Uploadscreenshot/',Upload_screenshot.as_view({'post':'create'})),
    path('Upload_document/',Upload_document.as_view({'post':'create'})),
    path('Checkattendence/',Checkattendenceview.as_view({'post':'create'})),
    path('Uploadprofilephoto/',Upload_profilephoto.as_view({'post':'create'})),
    path('Change_password/',ChangePasswordView.as_view() ,name='change-password'),
    path('Profile/',ProfileViewSet.as_view({'get': 'list'})),
    path('CreateForm/',Formviewset.as_view({'post': 'create'})),
    path('GetmyForm/',Formviewset.as_view({'get': 'list'})),
    path('Getpaymentdetials/',GetPaymentviewset.as_view({'get':'list'})),
    path('Attendence/',AttendenceviewSet.as_view({'get':'list','post': 'create'})),
    path('forgotpassword/',Forgotpasswordview.as_view({'post':'create'})),
    path('Updatesatedistrict/',Popupview.as_view({'post':'create'})),
    path('Getallstate/',Getallstate.as_view({'get': 'list'})),
    path('Getalldistrict/',Getalldistrict.as_view()),
    path('Getalltaluk/',Getalltaluk.as_view()),

]

