from rest_framework import serializers
from .models import UserInfo, UserEmbedding

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['user_seq', 'location', 'career', 'hobby', 'interest', 'personality']

class EmbeddedSeniorProfileSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer()
    
    class Meta:
        model = UserEmbedding
        fields = '__all__'
