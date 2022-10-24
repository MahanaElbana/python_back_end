# Python Back-End :rocket:

## Any Django Project :telescope: 

```
python3 -m venv env
```
```
source ./env/bin/activate
```
```
python3 -m pip install django
``` 
```
python3 -m pip install djangorestframework
```
```
pip freeze > requirements.txt
```
```
django-admin startproject project .
manage.py runserver 8001
python3 manage.py createsuperuser
```
```
$ pwd
```



```python


from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import re

class UserSerializer(serializers.ModelSerializer):
    '''
     - user = User.objects.create(**validated_data) = not hash password
     - user = User.objects.create_user(**validated_data) = hash password
     - save function execute [update or create]
    '''
    # To Make Email required  
    def email_required(value):
        if value is None:
            raise serializers.ValidationError('This field may not be blank.')
    
    # password strong
    def password_validator(value):
        if re.findall(r"^.*(?=.{16,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$", value) :
            pass
        else : raise serializers.ValidationError('password should contain captal letters ,small letters ,symbol from [@#$%^&+=] , digits at least 16 field')
    
    email = serializers.EmailField(
        validators =
          [ email_required ,
           UniqueValidator(queryset= User.objects.all() ,
           message="An email with that email already exists.") ]
       )
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        validators=[password_validator]
    )
    
    # To create new user (correct method)
    
    def create(self, validated_data):
        user = User.objects.create_user( is_active =False,**validated_data)
        return user
    
    # def create(self, validated_data):
    #     user = User(
    #         **validated_data
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    
    
    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    # def create(self , validated_data) :
    #     user = User.objects.create(
    #         username =validated_data['username'],
    #         email = validated_data['email']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user  
    
    # def save(self, **kwargs):
    #     '''
    #      - we can use save with out create or update
    #     '''
    #     user = super().save(**kwargs)
    #     user.set_password(self.validated_data['password'])
    #     user.save()
    #     return user 
    
    class Meta:
        # model which we take fields from .
        model = User
        # determined fields to manipulate
        fields = ('first_name' ,'username' ,'email' ,'password' ,'is_active') 
        read_only_fields = ['is_active']
        # extra_kwargs = {'password': {'write_only': True}  } 
       



'''
- required fields : 
   - password
   - username
{
        "password": "mahneyelbana",
        "last_login": null,
        "is_superuser": false,
        "username": "mahneyelbana",
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_staff": false,
        "is_active": false,
        "date_joined": "2022-10-23T03:24:02.298926Z",
        "groups": [],
        "user_permissions": []
}
'''    


class SendEmailVerficationSerializer(serializers.ModelSerializer):

    class Meta :
        model = User
        fields = ("email",)
        
    def validate(self, data):
        """
        Check that User is Exist.
        """
        user = User.objects.filter(email = data['email'] ).first()
        if user is None : 
            raise serializers.ValidationError("User is Not Exist")
         
        return {'email':user.email ,'username':user.username}     

class VerifyEmailOrEmailActivationAPIView():
    pass


class LogInSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(allow_blank=True, allow_null=True)
   
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
    ) 
   
    class Meta :
        model = User
        fields = ["email" ,"username" ,"password"]
        
    def validate(self, data):
          
        '''
        INFO :
         - print(data)
         - OrderedDict([('email', 'yor email'), ('username', 'your username'), ('password', 'your password')])
        '''  
        username = data.get('username').strip()
        email = data.get('email').strip()
        
        if username == "" and  email == "" : 
            raise serializers.ValidationError("At least enter one field from username and email.")  
          
        return data    
```


```python 
#from django.shortcuts import render




from .serializers import ( 
    UserSerializer ,
    SendEmailVerficationSerializer , LogInSerializer)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser  , IsAuthenticated
from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from .email import  send_otp_via_email


class IsAPIKey(permissions.BasePermission):
    message = 'IS Not API-kEY !'

    def has_permission(self, request, view):
        if str(request.user) == 'apikey':
            return True
        return False    

class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    permission_classes = [IsAPIKey,IsAuthenticated]

    def get(self,request, format=None):

        try:
           users = User.objects.all()
           serializer = UserSerializer(users, many=True)
           return Response(serializer.data)
        except:
             return Response('error')
    #apiKeyUser123456
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


def authorization_using_token(request):
           authorization_token = request.headers['Authorization']
           token = authorization_token[6:]
           userTokenObject = Token.objects.get(key= token)
           users = User.objects.filter(username= userTokenObject.user)
           return users 

class userItem(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self,request , format=None):
             

        try:
           print(request.group)
           # request.user in token and basic auth
           users =  users = User.objects.filter(username = request.user) 

           serializer = UserSerializer(users, many=True)
           return Response(serializer.data)
        except:
             return Response('error')   


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

    def post(self, request ):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            # user = serializer.create(validated_data=request.data)

            send_otp_via_email(email= user.email ,username= user.username)
            
            response_data =  {
                'user': serializer.data,
                'msge':'check your email verfication code'
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

    def post(self, request ):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')

            try :
              send_otp_via_email(email= email , username= username)
              return Response({"msg":"check your email verfication code "}, status=status.HTTP_201_CREATED)
           
            except :    
               return Response({"error":"resend code another"}, status=status.HTTP_400_BAD_REQUEST)
    
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

    def post(self, request ):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            print(serializer.data['password'])

            try :
              
              return Response(serializer.data, status=status.HTTP_201_CREATED)
           
            except :    
               return Response({"error":"resend code another"}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
          
```