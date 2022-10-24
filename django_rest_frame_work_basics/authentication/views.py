from rest_framework import status
from rest_framework.response import Response
from authentication.serializer import RegisterSerializer 
from rest_framework.generics import GenericAPIView


class RegisterAPIView(GenericAPIView):

    serializer_class = RegisterSerializer
    
    def post( self , request ) : 
        serializer = self.serializer_class(data =request.data)

        if serializer.is_valid():

            serializer.create(validated_data=serializer.data)

            return Response(serializer.data ,status=status.HTTP_201_CREATED)

        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)    