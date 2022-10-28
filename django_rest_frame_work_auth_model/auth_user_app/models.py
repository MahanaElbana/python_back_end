
from django.db import models
#from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User 
#from django.db.models.signals import post_save

# for email verification 
class EmailVerificationModel(models.Model):
    otp = models.IntegerField(null =True ,blank = True)
    #created_at = models.DateTimeField(default =datetime.now())
    created_at = models.DateTimeField(default =timezone.now())
    user = models.OneToOneField(User , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username 

#profile class 
class Profile(models.Model):
    user = models.OneToOneField(User , verbose_name ='user',on_delete=models.CASCADE)
    username = models.CharField(max_length =100 , null = True ,blank = True)
    first_name = models.CharField(max_length =100, null = True ,blank = True)
    last_name = models.CharField(max_length =100, null = True ,blank = True)
    email = models.EmailField( null = True ,blank = True)
    type = models.CharField(max_length =100,null = True ,blank = True)
    address = models.CharField(max_length =100 , null = True ,blank = True)
    
    def __str__(self) -> str:
        return self.user.username




