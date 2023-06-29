from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
User = get_user_model()

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
'''class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
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
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension'''
#---------------------------------------------------------------------------------------------------------------
class profileSerializer(serializers.ModelSerializer):
    profile_pic = Base64ImageField(max_length=None, use_url=True, )
    
    class Meta:
        model = UserProfile
        fields = ('profile_pic','mobile')
#---------------------------------------------------------------------------------------------------------------
#update profile and user
class UpdateUserSerializer(serializers.ModelSerializer):
    userprofile = profileSerializer()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'userprofile']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # Update only the fields of the user profile instance that are present in the request data
        instance.userprofile.__dict__.update((key, value) for key, value in userprofile_data.items() if value is not None)
        instance.userprofile.save()
        instance.save()

        return instance
'''class UpdateUserSerializer(serializers.ModelSerializer):
    userprofile = profileSerializer()
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','userprofile']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile', None)
        if userprofile_data is not None:
            instance.userprofile.profile_pic = userprofile_data['profile_pic']
            instance.userprofile.mobile = userprofile_data['mobile']
            # And save profile
            instance.userprofile.save()
        return super().update(instance, validated_data)'''
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
        return user
    '''def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
                user=user,
                profile_pic=profile_data['profile_pic'],
                mobile=profile_data['mobile'],
                
            )
        return user'''
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
#---------------------------------------------------------------------------------------
'''class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email','password')   '''

#---------------------------------------------------------------------------------------------------------------
'''class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128,min_length=8,write_only=True)
    #profile = profileSerializer(source="userprofile", many=False)

    class Meta:
        model = User
        fields = ('id','username','email','password',)
        read_only_fields = ('date_created', 'date_modified', 'id')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance'''

