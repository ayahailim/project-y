from django.shortcuts import render
from django.db import models
import cv2
import numpy as np
import keras
import tensorflow
from keras.models import Sequential
from keras.utils import img_to_array
import keras.utils
from keras.utils import load_img
from keras.models import Sequential, load_model
from .models import classifier
from .serializers import classifierSerializer
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import tempfile
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image

temp_model = load_model('./ml/7skin_model.h5')
print(temp_model.summary())
class classAPIView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    def post(self, format=None):
        classes = ['Basal Cell Carcinoma (BCC)', 'Melanocytic Nevi (NV)', 'Melanoma', 'Monkey Pox', 'Ringworm', 'Warts Molluscum,Viral Infections', 'normal']
        user = self.request.user
        serializer = classifierSerializer(data=self.request.data)
        if user.is_authenticated:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        image_file = self.request.FILES.get('image')
        print(image_file.read()) 
        if image_file:
            with io.BytesIO(image_file.read()) as image_bytes:
                
                image = Image.open(image_bytes).convert('RGB')
                image = image.resize((224, 224))
                image_array = np.array(image) / 255
                image_tensor = np.expand_dims(image_array, axis=0)
                prediction = temp_model.predict(image_tensor)
                max_pred = np.max(prediction)
                t = 0.95
                if max_pred < t:
                    prediction_label = "other diseases"
                else:
                    prediction_label = classes[np.argmax(prediction)]
            
                skin_image = classifier(user=user, image=image_file)
                skin_image.prediction = prediction_label
                print(skin_image.prediction)
                skin_image.save()
                serializer = classifierSerializer(skin_image)
                return Response(serializer.data) 
        else:
            return Response({'error': 'No image file provided.'}, status=400)

    '''def post(self, format=None):
        classes = ['Basal Cell Carcinoma (BCC)','Melanocytic Nevi (NV)','Melanoma','Monkey Pox','Ringworm','Warts Molluscum,Viral Infections','normal']
        user = self.request.user
        serializer = classifierSerializer(data=self.request.data)
        if user.is_authenticated:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        image_file = self.request.FILES.get('image')
        if image_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_file.read())
                temp_file.flush()
                temp_model = load_model('./ml/7skin_model.h5')
                test_image = load_img(temp_file.name, target_size=(224, 224))
                test_image = img_to_array(test_image) / 255
                test_image = np.expand_dims(test_image, axis=0)
                prediction = temp_model.predict(test_image)
                max_pred = np.max(prediction)
                t = 0.95
                if max_pred < t:
                    prediction_label = "other diseases"
                else:
                    prediction_label = classes[np.argmax(prediction)]

                skin_image = classifier.objects.create(user = user,image=image_file, prediction=prediction_label)
                serializer = classifierSerializer(skin_image)
                return Response(serializer.data) 
        else:
            return Response({'error': 'No image file provided.'}, status=400)''' 
        
























class classifierAPIView(generics.ListCreateAPIView):
    queryset = classifier.objects.all()
    serializer_class = classifierSerializer

    def perform_create(self, serializer):
        classes = ['Basal Cell Carcinoma (BCC)','Melanocytic Nevi (NV)',
                   'Melanoma','Monkey Pox','Ringworm','Warts Molluscum,Viral Infections','normal']
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user.id)
        else:
            serializer.save()
        image_file = self.request.FILES.get('image')
        if image_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_file.read())
                temp_file.flush()
                temp_model = load_model('./ml/7skin_model.h5')
                test_image = load_img(temp_file.name, target_size=(224, 224))
                test_image = img_to_array(test_image) / 255
                test_image = np.expand_dims(test_image, axis=0)
                prediction = temp_model.predict(test_image)
                max_pred = np.max(prediction)
                t = 0.95
                if max_pred < t:
                    prediction_label = "other diseases"
                else:
                    prediction_label = classes[np.argmax(prediction)]

                skin_image = classifier.objects.create(user = user.id, image=image_file, prediction=prediction_label)
                serializer = classifierSerializer(skin_image)
                return Response(serializer.data) 
        else:
            return Response({'error': 'No image file provided.'}, status=400) 
        
'''class classifierAPIView(generics.ListCreateAPIView):
    queryset = classifier.objects.all()
    serializer_class = classifierSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        classes = ['Basal Cell Carcinoma (BCC)','Melanocytic Nevi (NV)',
            'Melanoma','Monkey Pox','Ringworm','Warts Molluscum,Viral Infections','normal']
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            serializer.save()
        image_file = self.request.FILES.get('image')
        if image_file:
            try:
                if image_file.size == 0:
                    return Response({'error': 'The image file is empty.'}, status=400)
                img = Image.open(image_file)
                img.verify()
                img.close                
                temp_model = load_model('./ml/7skin_model.h5')
                test_image = load_img(image_file, target_size=(224, 224))
                test_image = img_to_array(test_image) / 255
                test_image = np.expand_dims(test_image, axis=0)
                prediction = temp_model.predict(test_image)
                max_pred = np.max(prediction)
                t = 0.95
                if max_pred < t:
                    prediction_label = "other diseases"
                else:
                
                    prediction_label = classes[np.argmax(prediction)]

                skin_image = classifier.objects.create(image=image_file, prediction=prediction_label, user=user)
                serializer = classifierSerializer(skin_image)
                return Response(serializer.data) 
            except (PIL.UnidentifiedImageError, OSError) as e:
                # Handle the error if the image file is empty, corrupted, or unsupported format
                return Response({'error': 'Unable to read image file.'}, status=400) 
        else:
            return Response({'error': 'No image file provided.'}, status=400)'''
        
'''class classifierAPIView(generics.ListCreateAPIView):
    queryset = classifier.objects.all()
    serializer_class = classifierSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        classes = ['Basal Cell Carcinoma (BCC)','Melanocytic Nevi (NV)',
                   'Melanoma','Monkey Pox','Ringworm','Warts Molluscum,Viral Infections','normal']
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            serializer.save()
        image_file = self.request.FILES.get('image')
        if image_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_file.read())
                temp_file.flush()
                temp_model = load_model('./ml/7skin_model.h5')
                test_image = load_img(temp_file.name, target_size=(224, 224))
                test_image = img_to_array(test_image) / 255
                test_image = np.expand_dims(test_image, axis=0)
                prediction = temp_model.predict(test_image)
                max_pred = np.max(prediction)
                t = 0.95
                if max_pred < t:
                    prediction_label = "other diseases"
                else:
                    prediction_label = classes[np.argmax(prediction)]
                skin_image = serializer.create(user = user, image=image_file, prediction=prediction_label )
                serializer = classifierSerializer(skin_image)
                return Response(serializer.data)
        else:
            return Response({'error': 'No image file provided.'}, status=400)'''
        
'''user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            serializer.save()
        image_file = self.request.FILES.get('image')
        if image_file:
            with Image.open(image_file) as img:
                temp_model = load_model('./ml/7skin_model.h5')
                test_image = load_img(img, target_size=(224, 224))
                test_image = img_to_array(test_image) / 255
                test_image = np.expand_dims(test_image, axis=0)
                prediction = temp_model.predict(test_image)
                max_pred = np.max(prediction)
                t = 0.95
                if max_pred < t:
                    prediction_label = "other diseases"
                else:
                    prediction_label = classes[np.argmax(prediction)]

                skin_image = classifier.objects.create(image=img, prediction=prediction_label, user = user)
                serializer = classifierSerializer(skin_image)
                return Response(serializer.data) 
        else:
            return Response({'error': 'No image file provided.'}, status=400)'''

#-------------------------------------
'''def get(self, request):
        try:
            classifier = classifier.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'fetched successfully',
                'data': [{
                    'user':classifier.user,
                    'image': classifier.image.url,
                    'date': classifier.date,
                    'prediction': classifier.prediction,
            
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