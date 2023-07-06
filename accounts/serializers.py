from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
User = get_user_model()
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.core.files.base import ContentFile
import base64
import six
import uuid

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            # Check if the base64 data is empty
            if data.strip() == '':
                return None

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
#---------------------------------------------------------------------------------------------------------------
class profileSerializer(serializers.ModelSerializer):
    profile_pic = Base64ImageField(max_length=None, use_url=True, )
    profile_pic = serializers.ImageField(required=False, allow_empty_file=True)
    class Meta:
        model = UserProfile
        fields = ('profile_pic','mobile')
        extra_kwargs = {'mobile': {'required': False}}
#---------------------------------------------------------------------------------------------------------------
#update profile and user
class UpdateUserSerializer(serializers.ModelSerializer):
    userprofile = profileSerializer()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'userprofile']
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        'username': {'required': False},
                        'email': {'required': False}}

    def validate_email(self, value):
        """
        Validate that the email address is valid if provided.
        """
        if value:
            try:
                validate_email(value)
            except ValidationError:
                raise serializers.ValidationError('Invalid email address.')
        return value

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile', {})
        
        # Update the username field if it is included in the request data
        username = validated_data.get('username', None)
        if username is not None:
            instance.username = username
        
        # Update the email field if it is included in the request data and not empty
        email = validated_data.get('email', None)
        if email:
            instance.email = email
        
        # Update only the fields of the user profile instance that are present in the request data
        instance.userprofile.__dict__.update((key, value) for key, value in userprofile_data.items() if value is not None)
        instance.userprofile.save()
        instance.save()

        return instance

#---------------------------------------------------------------------------------------------------------------
#sign up 
class RegisterSerializer(serializers.ModelSerializer):
    profile = profileSerializer(required=False)

    class Meta:
        model = User
        fields = ('username','email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)
        profile_pic = profile_data.get('profile_pic', 'default_profile_pic.jpg')
        mobile = profile_data.get('mobile')
        UserProfile.objects.create(
            user=user,
            profile_pic=profile_pic,
            mobile=mobile,
        )
        return user   
#---------------------------------------------------------------------------------------------------------------
#change password
class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
#-----------------------------------------------------------------------------------------
'''class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],validated_data['email'], validated_data['password'])

        return user
    '''
'''class RegisterSerializer(serializers.ModelSerializer):
    profile = profileSerializer(required=False)

    class Meta:
            model = User
            fields = ('username','email', 'password', 'profile')
            extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)
        if 'profile_pic' in profile_data and profile_data['profile_pic'] != '':
            profile_pic = profile_data['profile_pic']
        else:
            profile_pic = 'default_profile_pic.jpg'
        mobile = profile_data.get('mobile')
        UserProfile.objects.create(
            user=user,
            profile_pic=profile_pic,
            mobile=mobile,
        )
        return user'''
'''rclass RegisterSerializer(serializers.ModelSerializer):
    profile = profileSerializer(required=False)

    class Meta:
        model = User
        fields = ('username','email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)
        profile_pic = profile_data.get('profile_pic')
        if profile_pic is not None and profile_pic != '':
            pass
        else:
            profile_pic = 'default_photo.jpg'
        mobile = profile_data.get('mobile')
        UserProfile.objects.create(
            user=user,
            profile_pic=profile_pic,
            mobile=mobile,
        )
        return user'''