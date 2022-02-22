from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    rolename = models.CharField(max_length=30)
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given mobile_number must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    mobile_number = models.CharField(max_length=15,unique=True)
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    profile_photo = models.FileField(null=True)
    role_id = models.IntegerField(null=True)
    role = models.CharField(max_length=20,null=True,default='user')
    otp = models.IntegerField(null=True)
    otp_expiry = models.DateTimeField(null=True)
    state_id = models.IntegerField(null=True)
    district = models.CharField(null=True,max_length=50)
    state = models.CharField(max_length=20,null=True)
    city = models.CharField(max_length=30,null=True)
    taluk = models.CharField(max_length=50,null=True)
    email_token = models.CharField(max_length=255,null=True)
    pincode = models.IntegerField(null=True)
    talukhead_id = models.IntegerField(null=True)
    statehead_id = models.IntegerField(null=True)
    designation_id = models.IntegerField(null=True)
    districthead_id = models.IntegerField(null=True)
    is_otpvalidated = models.BooleanField(default=False,null=False)
    document_photo = models.FileField(null=True)

    is_verified = models.BooleanField(default=False,null=True)

    is_formupdated = models.BooleanField(default=False,null=True)

    payment_photo = models.FileField(null=True)
    is_paymentdone = models.BooleanField(default=False,null=True)
    payment_verified = models.BooleanField(null=True,default=False)
    approved_by = models.CharField(max_length=100,null=True)
    form_verified = models.BooleanField(null=True,default=False)
    is_Admin = models.BooleanField(null=True,default=False)
    is_staff = models.BooleanField(null=True,default=False)

    assigned_stateid = models.IntegerField(null=True)
    assigned_districtid = models.IntegerField(null=True)
    assigned_talukid = models.IntegerField(null=True)
    district_id = models.IntegerField(null=True)
    state_updated = models.BooleanField(null=True,default=False)
    taluk_id = models.IntegerField(null=True)
    objects = CustomUserManager()


    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            #'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

education_choices = (
    ('Below 10th','Below 10th'),
    ('10th','10th'),
    ('12th','12th'),
    ('Diploma','Diploma'),
    ('Undergraduate','Undergraduate'),
    ('Postgraduate','Postgraduate'),
)

class Form(models.Model):
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    qualification = models.CharField(max_length=50,null=True)
    aadhar_no = models.CharField(max_length=12,null=True)
    address = models.TextField()
    csc_id = models.BooleanField(null=True)
    csc_id_number = models.CharField(max_length=50,null=True)
    bc_id = models.BooleanField(null=True)
    bc_id_number = models.CharField(max_length=50,null=True)
    csp_id = models.BooleanField(null=True)
    csp_id_number = models.CharField(max_length=50,null=True)
    district = models.CharField(null=True,max_length=50)
    district_id = models.IntegerField(null=True)
    state_id = models.IntegerField(null=True)
    taluk_id = models.IntegerField(null=True)
    state = models.CharField(max_length=20,null=True)
    city = models.CharField(max_length=30,null=True)
    taluk = models.CharField(max_length=50,null=True)
    pincode = models.IntegerField(null=True)
    pan_number = models.CharField(max_length=50)
    document_photo = models.FileField(null=True)
    terms_condition = models.BooleanField(default=False,null=False)

    form_verified = models.BooleanField(null=True,default=False)
    updated_on = models.DateField(auto_now_add=True)
    createdby = models.CharField(max_length=100)


class Attendence(models.Model):
    date= models.DateField()
    status = models.BooleanField(default=False,null=True)
    user_id = models.CharField(max_length=100)


class Payment(models.Model):
    phone_pe_number = models.CharField(max_length=20)
    google_pay_number = models.CharField(max_length=20)
    upi_id = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    qr_code = models.FileField(null=True)
    state = models.CharField(max_length=100)
    state_id = models.IntegerField(null=True)


class Sample(models.Model):
    is_boolean = models.BooleanField(null=True,default=False)

class State_master(models.Model):
    id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=50)


class District_master(models.Model):
    id = models.AutoField(primary_key=True)
    state_id = models.IntegerField(null=True)
    district_name = models.CharField(max_length=100)

class Taluk_master(models.Model):
    id = models.AutoField(primary_key=True)
    state_id = models.IntegerField(null=True)
    district_id = models.IntegerField(null=True)
    taluk_name = models.CharField(max_length=50)
