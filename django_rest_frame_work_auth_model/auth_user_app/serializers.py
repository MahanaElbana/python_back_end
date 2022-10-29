

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


class LogInUserNameSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(allow_blank=False, allow_null=False)
   
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
    ) 
   
    class Meta :
        model = User
        fields = ["username" ,"password"]
        
    #def validate(self, data):
    #      
    #    '''
    #    INFO :
    #     - print(data)
    #     - OrderedDict([('email', 'yor email'), ('username', 'your username'), ('password', 'your password')])
    #    '''  
    #    username = data.get('username').strip()
    #    email = data.get('email').strip()
    #    
    #    if username == "" and  email == "" : 
    #        raise serializers.ValidationError("At least enter one field from username and email.")  
    #      
    #    return data    