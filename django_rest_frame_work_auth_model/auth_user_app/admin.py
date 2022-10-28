from django.contrib import admin
from .models import EmailVerificationModel ,Profile
# Register your models here.

admin.site.register(EmailVerificationModel)
admin.site.register(Profile)