

from .serializers import (
    UserSerializer,
    SendEmailVerficationSerializer,
    LogInSerializer)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import  IsAuthenticated
from auth_user_app.authentication import JWTAuthentication    # for access token
from rest_framework.authentication import TokenAuthentication # for refresh token
from django.contrib.auth.models import User


from .email import send_otp_via_email

#! Login
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# from auth_user_app.jwt_tokens import create_token
# import jwt

''' -------------------------------------------------------------- '''
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
    authentication_classes = [JWTAuthentication]

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
# [1] Create New an account (SignUp)


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
class LogInAPIView(APIView):
    '''
    log in using ( email or username ) and password
    '''
    serializer_class = LogInSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            print(serializer.data['password'])

            try:
                username = serializer.validated_data.get("username")
                password = serializer.validated_data.get("password")
                # if username is ""  :
                #  print("true user is none")
                user = authenticate(
                    request, username=username, password=password)

                if user is None:
                    return Response({"error": "Invalid authentication creadintial !"}, status=status.HTTP_400_BAD_REQUEST)

                #created_token =  create_token(user.username)
                #instance_token = Token.objects.create(key = created_token , user =user)
                instance_token = Token.objects.get(user=user)
                instance_token.delete()

                return Response({'token': instance_token.key, 'username': username}, status=status.HTTP_201_CREATED)

            except:
                return Response({"error": "resend code another"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
