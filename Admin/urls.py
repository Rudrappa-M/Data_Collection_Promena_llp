from django.urls import path,include
from rest_framework_swagger.views import get_swagger_view
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
# from django.conf.urls import url

urlpatterns = [


    
    path('Login/',LoginAPIView.as_view() ),
    path('Getallusers/',Get_allusers.as_view({'get':'list'})),
    #path('GetallWorkers/',GetallWorkers.as_view({'get':'list'})),
    path('Getallstatehead/',Getallstatehead.as_view({'get':'list'})),
    path('Getalltalukhead/',Getalltalukhead.as_view({'get':'list'})),
    path('Getalldistricthead/',Getalldistricthead.as_view({'get':'list'})),
    path('Getallforms/',Getallforms.as_view({'get':'list'})),
    path('Paymentdetailsallstates/',Paymentdetailsallstates.as_view({'get':'list'})),
    path('Paymentdetails/',Paymentdetails.as_view({'get':'list'})),
    path('GetFormbyid/',GetFormbyid.as_view()),
    path('CreateRole/',CreateRolesview.as_view({'post':'create'})),
    path('AssignRole/',AssignRoleview.as_view({'post':'create'})),
    path('Requestupdateform/',Requestupdateform.as_view({'post':'create'})),
    path('Verifyuser/',VerifyuserViewSet.as_view({'post':'create'})),
    path('Paymentverifyuser/',PaymentverifyuserViewSet.as_view({'post':'create'})),
    path('Formverifyuser/',FormverifyuserViewSet.as_view({'post':'create'})),
    path('GetRoles/',Rolesview.as_view({'get':'list'})),
    path('Getuserstatus/',Getuserstatus.as_view()),
    path('UpdateRoles/',Rolesview.as_view({'put':'update'})),
    path('DeleteRoles/',DeleteRole.as_view()),
    path('Getallstates/',Getallstates.as_view({'get':'list'})),
    path('Getalldistricts/',Getalldistricts.as_view()),
    path('Getallattendance/',Getallattendance.as_view()),
    path('Getalltaluks/',Getalltaluks.as_view()),
    #path('Deletestate/',Deletestate.as_view()),
    path('Createpaymentdetials/',Postpayment.as_view({'post':'create'})),
    path('Uploadprofilephoto/',Upload_profilephoto.as_view({'post':'create'})),
    path('Updatepaymentdetials/',Updatepaymentdetials.as_view({'put': 'update'})),
    path('UploadQrphoto/',Upload_QRcode.as_view({'post':'create'})),
    path('Change_password/',ChangePasswordView.as_view() ,name='change-password'),
    path('Createusers/',CreateUsers.as_view({'post': 'create',})),
    path('Profile/',Profile.as_view({'get': 'list'})),
    path('forgotpassword/',Forgotpasswordviews.as_view({'post':'create'})),
    path('resetpassword/',Password_reset.as_view()),
    path('Deleteform/',Deleteform.as_view()),


]
