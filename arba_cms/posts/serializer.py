from rest_framework import serializers
from .models import ImagePost, Comment

class ImagePostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = ImagePost
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    image_post_id = serializers.CharField(source='imagepost.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'