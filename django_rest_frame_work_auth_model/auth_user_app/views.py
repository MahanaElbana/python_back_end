

from .serializers import (GenerateAccessTokenSerializer, 
                          UserSerializer,
                          SendEmailVerficationSerializer,
                          LogInUserNameSerializer ,VerifyEmailOrEmailActivationSerializer)

from auth_user_app.jwt_tokens import (create_access_token,
                                      create_access_refresh_token)

from auth_user_app.models import EmailVerificationModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from auth_user_app.authentication import JWTAuthentication ,JWTRefreshAuthentication   # for access token
from rest_framework.authentication import TokenAuthentication  # for refresh token
from django.contrib.auth.models import User


from .email import send_otp_via_email

#! Login
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# import jwt

''' -------------------------------------------------------------- '''
# [1] GET authorized user"s profile details
class UserDetails(APIView):
    """
    URL : http://127.0.0.1:8001/auth/api/user/
    Method : GET
    API View to  get a user details .
    GET request returns the registered user .
    GET authorized user details 
    -- --- under updating using Profile --- --- 
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] # Bearer or Token
    ## ---------------- swagger ------------------------##
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    ## --------------------------------------------------##
    def get(self, request):
        print(request.user)
        try:
            user = request.user
            user_filterd = User.objects.filter(
                username=user.username, email=user.email)
            serializer = UserSerializer(user_filterd, many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except:
            return Response({'error': 'user is not exist'})


''' -------------------------------------------------------------- '''
# [2] Create New an account (SignUp)
class RegisterAPIView(APIView):
    '''
    URL : http://127.0.0.1:8001/auth_user_app/register/
    Method : POST
    Required body data (json) : 
      {
       "username":"your user name" ,
      "email":"your email"
      'first_name':"your frist name" ,
      'password':"password"
      }
    '''
    serializer_class = UserSerializer
    ## ---------------- swagger ------------------------##
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    ## --------------------------------------------------##
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # user = serializer.create(validated_data=request.data)

            send_otp_via_email(email=user.email, username=user.username)

            response_data = {
                'user': serializer.data,
                'msge': 'check your email verfication code'
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' -------------------------------------------------------------- '''
# [3] Send  otp code to gmail  (code to active email)
class SendEmailVerficationAPIView(APIView):
    '''
      -- send otp code to user email to active your email -- 

    URL : http://127.0.0.1:8001/auth_user_app/SendEmailVerfication/
    Method : POST
    Required body data (json) : {"email":"your email"}
    '''
    serializer_class = SendEmailVerficationSerializer
    ## ---------------- swagger ------------------------##
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    ## --------------------------------------------------##
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')

            try:
                send_otp_via_email(email=email, username=username)
                return Response({"msg": "check your email verfication code "}, status=status.HTTP_201_CREATED)

            except:
                return Response({"error": "resend code another"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

''' -------------------------------------------------------------- '''
# [4] Email verfication or Email activation
class VerifyEmailOrEmailActivationAPIView(APIView):
    '''
      -- active email using otp code -- 

    URL : http://127.0.0.1:8001/api/auth/EmailOTPpVerfication/
    Method : PUT
    Required body data (json) : {"email":"your email" , "otp":"your otp"}
    '''
    serializer_class = VerifyEmailOrEmailActivationSerializer
    ## ---------------- swagger ------------------------##
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    ## --------------------------------------------------##
    def put(self , request ):
        
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            
            email = serializer.validated_data.get('email')
            otp_code = serializer.validated_data.get('otp')
            
            #  Does that user exist or not?
            try : 
               user = User.objects.get(email = email)
            except User.DoesNotExist as error: 
                return Response({'error':str(error)}, status=status.HTTP_400_BAD_REQUEST)
            
            #  Does that emailVerificationModel exist or not?
            try: 
                emailVerificationModel = EmailVerificationModel.objects.get(user =user)
            except EmailVerificationModel.DoesNotExist as error: 
                return Response({'error':str(error)}, status=status.HTTP_400_BAD_REQUEST)    
            
            # email activation
            try:
                
                if otp_code != emailVerificationModel.otp : 
                    raise Exception("otp is not correct !")
                
                user.is_active = True
                user.save()
               
                return Response(
                    {**serializer.data ,"is_active":str(user.is_active) , 
                      "username" : user.username},
                       status=status.HTTP_201_CREATED)
            
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

''' -------------------------------------------------------------- '''

# [5] log in using username and password 
class LogInUserNameAPIView(APIView):
    '''
    log in using (username ) and password 
    '''
    serializer_class = LogInUserNameSerializer
    
   ## ---------------- swagger ------------------------##
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    ## --------------------------------------------------##
    def post(self, request  ):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            print(serializer.data['password'])

            try:
                username = serializer.validated_data.get("username")
                password = serializer.validated_data.get("password")

                user = authenticate(
                    request, username=username, password=password)

                if user is None:
                    return Response({"error": "Invalid authentication creadintial !"}, status=status.HTTP_400_BAD_REQUEST)

                # Check that the email is verified .
                try:
                    if user.is_active == False:

                        raise Exception('active your email firstly !')
                except Exception as error:
                    return Response({'error': str(error)})

                try:

                    # Check if a refresh token exists.
                    instance_refresh_token_isExist = Token.objects.filter(
                        user=user).first()

                    if instance_refresh_token_isExist is not None:
                        raise Exception('logout firstly !')

                    # make a refresh and an access token .
                    created_ref_acc_token = create_access_refresh_token(
                        user.username)

                    # store the refresh token in the token model.
                    instance_token = Token.objects.create(
                        key=created_ref_acc_token['refresh'], user=user)

                except Exception as error:
                    return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

                return Response({'refresh': instance_token.key,
                                 'access': created_ref_acc_token['access'],
                                 'username': username}, status=status.HTTP_201_CREATED)

            except:
                return Response({"error": "resend code another"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


''' generate access token using refresh token API View '''
# [6] re_generate access token
class GenerateAccessTokenAPIView(APIView):
      
    serializer_class = GenerateAccessTokenSerializer
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTRefreshAuthentication] 
    ## ---------------- swagger ------------------------##
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    ## --------------------------------------------------##
    def get(self, request, format=None):
        print(request.user)
        try:
            user = request.user
            created_acc_token = create_access_token(user.username)

            user_filterd = Token.objects.filter(user = user).first()
            serializer = self.serializer_class(user_filterd)
            return Response(
                {"refresh":serializer.data['key'] , "access":created_acc_token} , status= status.HTTP_202_ACCEPTED)
        except:
            return Response({'error': 'user is not exist' } , status= status.HTTP_400_BAD_REQUEST)
      
''' ---------------------------------------------------------------------------'''
# [7] logout API VIEW
class LogoutView(APIView):
    
    serializer_class = GenerateAccessTokenSerializer
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTRefreshAuthentication] 
    ## ---------------- swagger ------------------------##
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    ## --------------------------------------------------##
    def delete(self, request):
        user = request.user
        token = Token.objects.filter(user = user).first()
        token.delete()
        return Response({'error': 'user is not exist' } , status= status.HTTP_400_BAD_REQUEST)