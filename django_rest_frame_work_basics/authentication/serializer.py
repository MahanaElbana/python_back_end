
from rest_framework import serializers
from authentication.models import User

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 125 , min_length = 6 ,write_only = True ,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
    )

    class Meta :
        model = User 
        fields = ('username' ,'email' ,'password' ) 