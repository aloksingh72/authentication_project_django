from django.db import models

# Create your models here.
class UserDetails(models.Model):
    username = models.CharField(max_length =100,unique = True)
    email= models.EmailField(max_length =100,unique =True)
    password = models.CharField(max_length=100)
    confirm_password= models.CharField(max_length =100)
    created_on = models.DateTimeField(auto_now_add = True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    class Meta:
        db_table = "user_details"

    