from rest_framework.views import APIView
from . import serializers
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import permissions

from extensions.handler import SuccessResponse, FailureResponse


# Create your views here.


class RegisterUserAPIView(generics.CreateAPIView):
            
    serializer_class = serializers.RegisterSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_serializer = serializers.UserSerializer(user, many=False)

        return SuccessResponse(response_serializer.data, 200).response()


class LoginUserAPIView(APIView):

    def post(self, request):
        
        serializer = serializers.LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
    
        token = Token.objects.get(user=user)

        return SuccessResponse(token.key, 200).response()



class UserDetailAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        serializer = serializers.UserSerializer(request.user, many=False)
        return SuccessResponse(serializer.data, 200).response()