from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import *
# Create your models here.
class UserDetails(AbstractBaseUser):
    username = models.CharField(max_length =100,unique = True)
    email= models.EmailField(max_length =100,unique =True)
    password = models.CharField(max_length=100)
    confirm_password= models.CharField(max_length =100)
    created_on = models.DateTimeField(auto_now_add = True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    is_active =models.BooleanField(default = True)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # add any required fields besides email




    class Meta:
        db_table = "user_details"

    