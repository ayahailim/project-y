from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import  RegisterSerializer ,ChangePasswordSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView 
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UpdateUserSerializer
from rest_framework.exceptions import AuthenticationFailed
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view
User = get_user_model()
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.contrib.auth import authenticate
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

#---------------------------------------------------------------------------------------------------
#sign_up page

class RegisterAPI(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User registered  successfully',
            }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)
#---------------------------------------------------------------------------------------------------
# login page

class CustomAuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Username or password is incorrect')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg, code='authorization')

            attrs['user'] = user
            return attrs
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token = AuthToken.objects.create(user)[1]
            return Response({'message': 'successfully logged in', 'token': token})
        else:
            return Response(serializer.errors, status=400)
#---------------------------------------------------------------------------------------------------
#update profile and user togther

class UpdateUser(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer
    queryset = get_user_model().objects.all()
    

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj
    
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    
#---------------------------------------------------------------------------------------------------
#change password
class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status= status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
#---------------------------------------------------------------------------------------------------

























