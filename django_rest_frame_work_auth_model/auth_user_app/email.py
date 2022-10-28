
from django.core.mail import send_mail
from random import randint
from django.conf import settings
from django.contrib.auth.models import User
from .models import EmailVerificationModel
from datetime import datetime


def send_otp_via_email(email , username):
    subject = 'Your account verfication email '
    otp_code = randint(100000, 999999)
    message = f'Your otp code is {otp_code}'
    email_from = settings.EMAIL_HOST

    send_mail(
        subject=subject,
        message=message,
        from_email =email_from, 
        recipient_list=[email], 
        fail_silently=False )

    '''
     - User Model 
     - EmailVerificationModel
     - to make email is active 
    '''
    user = User.objects.filter(email= email ,username =username).first()
    email_verfication_user = EmailVerificationModel.objects.filter(user = user).first()
    
    if email_verfication_user is None : 
        EmailVerificationModel.objects.create(
        otp=otp_code, created_at=datetime.now(), user=user
        )
    
    else : 
        email_verfication_user.otp = otp_code
        email_verfication_user.created_at = datetime.now()
        email_verfication_user.save()
    


# from django.core.mail import EmailMessage


# import threading


# class EmailThread(threading.Thread):

#     def __init__(self, email):
#         self.email = email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()


# class Util:
#     @staticmethod
#     def send_email(data):
#         email = EmailMessage(
#             subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
#         EmailThread(email).start()
