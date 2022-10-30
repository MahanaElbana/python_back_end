

from .serializers import (GenerateAccessTokenSerializer, 
                          UserSerializer,
                          SendEmailVerficationSerializer,
                          LogInUserNameSerializer)
from auth_user_app.jwt_tokens import (create_access_token,
                                      create_access_refresh_token)
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

    def get(self, request, format=None):
        print(request.user)
        try:
            user = request.user
            user_filterd = User.objects.filter(
                username=user.username, email=user.email)
            serializer = UserSerializer(user_filterd, many=True)
            return Response(serializer.data)
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


# [2] Send  otp code to gmail  (code to active email)
class SendEmailVerficationAPIView(APIView):
    '''
      -- send otp code to user email to active your email -- 

    URL : http://127.0.0.1:8001/auth_user_app/SendEmailVerfication/
    Method : POST
    Required body data (json) : {"email":"your email"}
    '''
    serializer_class = SendEmailVerficationSerializer

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


# [3] Email verfication ot Email activation
class VerifyEmailOrEmailActivationAPIView(APIView):
    '''
      -- active email using otp code -- 

    URL : http://127.0.0.1:8001/auth_user_app/SendEmailVerfication/
    Method : PUT
    Required body data (json) : {"email":"your email"}
    '''
    serializer_class = SendEmailVerficationSerializer

    def put():
        pass


# [4]
class LogInUserNameAPIView(APIView):
    '''
    log in using (username ) and password
    '''
    serializer_class = LogInUserNameSerializer

    def post(self, request):

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
# [5] re_generate access token
class GenerateAccessTokenAPIView(APIView):
      
    serializer_class = GenerateAccessTokenSerializer
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTRefreshAuthentication] 
    
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
      
