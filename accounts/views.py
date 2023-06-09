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
#from rest_framework.authentication import BasicAuthentication
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view
User = get_user_model()

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
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token = AuthToken.objects.create(user)[1]
        return Response({'message': 'successfully logged in', 'token': token})
# login page
'''class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)'''
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




























'''class UserAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes=[BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'data': [{
                    'username': user_profile.user.username,
                    'email': user_profile.user.email,
                    'password': user_profile.user.password,
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'profile_pic': user_profile.profile_pic.url,
                    'mobile': user_profile.mobile,
            
                    }]
                }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)
    def get_object(self):
        return self.request.user '''   
#---------------------------------------------------------------------------------------------------
'''class MultipleFieldLookupMixin:
   
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj   
class UserRetrieveUpdateAPIView(MultipleFieldLookupMixin,generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)'''
#---------------------------------------------------------------------------------------------------
# Register API
'''class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })'''
#---------------------------------------------------------------------------------------------------
'''class IsAuthenticatedOrWriteOnly(BasePermission):
    def has_permission(self, request, view):
        WRITE_METHODS = ["POST", ]

        return (
            request.method in WRITE_METHODS or
            request.user and
            request.user.is_authenticated
        )
class UserList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrWriteOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''
#---------------------------------------------------------------------------------------------------
#profile page
'''
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'profile_pic': user_profile.profile_pic.url,
                    'mobile': user_profile.mobile,
            
                    }]
                }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)'''
#---------------------------------------------------------------------------------------------------
'''class updateuserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    #permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user '''
#--------------------------------------------------------------------------------------------
'''class updateprofileView(RetrieveUpdateAPIView):
    serializer_class = profileSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user '''
#---------------------------------------------------------------------------------------------------