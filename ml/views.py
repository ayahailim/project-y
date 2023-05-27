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
from .models import preuser
from .serializers import preuserSerializer
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import tempfile
from rest_framework.permissions import IsAuthenticated
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image

'''class classifierAPIView(APIView):
    def post(self,request):
        classes = ['Basal Cell Carcinoma (BCC)','Melanocytic Nevi (NV)','Melanoma','Monkey Pox','Ringworm','Warts Molluscum,Viral Infections','normal']
        image_file = request.FILES.get('image')
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
                
                classifier.objects.create(image=image_file, prediction=prediction_label)
                return Response({'Disease': prediction_label}, status=200)
        else:
            return Response({'error': 'No image file provided.'}, status=400) '''

             

class classAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        preuser_objects = preuser.objects.filter(user=user)
        serializer = preuserSerializer(preuser_objects, many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        classes = ['Basal Cell Carcinoma (BCC)','Melanocytic Nevi (NV)','Melanoma','Monkey Pox','Ringworm','Warts Molluscum,Viral Infections','normal']
        image_file = request.FILES.get('image')
        user = request.user
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
                t = 0.90
                if max_pred < t:
                    prediction_label = "other diseases"
                else:
                    prediction_label = classes[np.argmax(prediction)]
                
                preuser.objects.create(user=user,image=image_file, prediction=prediction_label)
                return Response({'Disease': prediction_label}, status=200)
        else:
            return Response({'error': 'No image file provided.'}, status=400) 
        