from rest_framework import serializers
from accounts.models import UserProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):

    class Meta:
    
        model = UserProfile
        fields = ["id", "first_name", "last_name", "username", "email", "is_staff"]


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )

    class Meta:

        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'password', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
        
    def create(self, validated_data):

        user = UserProfile.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])

        Token.objects.create(user=user)  

        user.save()
        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = ('Invalid Credentials')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Username or Password is missing')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data