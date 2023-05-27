from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields =('id', 'message', 'user', 'stars')
        read_only_fields = ('id', 'user')
