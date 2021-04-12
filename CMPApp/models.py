from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.utils import timezone
# Create your models here.

class CollegeData(models.Model):
    enroll = models.CharField(max_length=12,blank=False)
    fname = models.CharField(max_length=20,blank=False)
    lname = models.CharField(max_length=20,blank=False)
    email = models.EmailField(max_length=50,blank=False)
    dept = models.CharField(max_length=20,blank=False)
    grad_year = models.IntegerField(blank=False)

    def __str__(self):
        return self.enroll

class UserProfileManager(BaseUserManager):
    '''user profile manager'''

    def create_user(self,email,fname,password,lname,enroll,dept,grad_year,verification_code=None,is_Email_Verified=False):
        '''creating user model'''
        if not email:
            raise ValueError("Email field is required")

        email=self.normalize_email(email)
        user=self.model(email=email,fname=fname,lname=lname,enroll=enroll,dept=dept,grad_year=grad_year,verification_code=verification_code,is_Email_Verified=is_Email_Verified)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,fname,password):
        '''creating superuser for user profile'''

        user=self.create_user(email,fname,password)

        user.is_staff=True
        user.is_superuser=True

        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''Database model for users in thr system'''

    email = models.EmailField(max_length=255,unique=True)
    fname = models.CharField(max_length=20,blank=False,null=False)
    lname = models.CharField(max_length=20,blank=False,null=True)
    enroll = models.CharField(max_length=12,blank=False,null=True)
    dept = models.CharField(max_length=10,blank=False,null=True)
    grad_year = models.IntegerField(blank=False,null=True)
    # Roll_fac = models.CharField(max_length=20,blank=True,null=True)
    # mobile = models.CharField(max_length=10,blank=True,null=True)
    password = models.CharField(max_length=20)
    verification_code = models.CharField(max_length=50,blank=True,null=True)
    is_Email_Verified = models.BooleanField(default=False)
    # document = models.FileField(upload_to='documents/')
    avtar = models.ImageField(upload_to='user_image/',blank=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname']

    def get_full_name(self):
        '''Retrieve full name of user'''
        return self.fname + " " + self.lname

    # def get_short_name(self):
    #     '''Retrieve short name of the user'''
    #     return self.Name

    def __str__(self):
        return self.enroll


class Resource(models.Model):
    Title = models.CharField(max_length=50,blank=False,null=True)
    Category = models.CharField(max_length=50,blank=False,null=True)
    DP = models.ImageField(upload_to='book_image/',blank=False)
    Description = models.TextField(default="",blank=False)
    Type = models.CharField(default="Free",max_length=50)
    Price = models.IntegerField(default=0,blank=False)
    Branch = models.CharField(max_length=50,blank=False,null=True)
    # uploaded_at = models.DateTimeField(blank=True, auto_now_add=True,null=True)
    user = models.ForeignKey(UserProfile, blank=False,on_delete=models.CASCADE)
    isbn = models.CharField(max_length=20,blank=False,null=True,default="NA")

    def __str__(self):
        return self.Title + "_" + str(self.id)

class requestedResources(models.Model):
    don = models.CharField(max_length=12,blank=False,null=True)
    req = models.ForeignKey(UserProfile, blank=False,null=True,on_delete=models.CASCADE)
    res = models.ForeignKey(Resource, blank=False,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.req.enroll + "_" + self.don + "_" + self.res.Title


class newRequest(models.Model):
    req = models.ForeignKey(UserProfile,blank=False,null=True,on_delete=models.CASCADE)
    isbn = models.CharField(max_length=20,blank=False,null=True,default="NA")

    def __str__(self):
        return self.req.enroll + "_" + self.isbn

class contactUs(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(max_length=50,blank=False)
    subject = models.CharField(max_length=50,blank=True)
    suggestion = models.TextField(default="",blank=False)

    def __str__(self):
        return str(self.id) + "_" + self.name
