from auth_user_app.jwt_tokens import decode_data # jwt functionality

from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
import jwt 

class JWTAuthentication(authentication.BaseAuthentication):
  
   def authenticate(self, request):

        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            raise exceptions.AuthenticationFailed('you not autherized , login !')
        
        try :
            prefix, access_token = auth_data.decode('utf-8').split(' ')   
        except : 
            raise exceptions.AuthenticationFailed('adadsd')

        try : 
            payload = decode_data(access_token)

        except jwt.exceptions.ExpiredSignatureError as expired_error:
            raise  exceptions.AuthenticationFailed(str(expired_error))
              
        except jwt.exceptions.InvalidSignatureError as Invalid_signature_error:
            raise exceptions.AuthenticationFailed(str(Invalid_signature_error)) 
        
        except jwt.exceptions.DecodeError as decode_error:
            raise exceptions.AuthenticationFailed(str(decode_error)) 
         
        try:     
            username = payload['username']
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
 
        return (user, None)

