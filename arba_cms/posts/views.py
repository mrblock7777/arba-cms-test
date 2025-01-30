from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImagePost, Comment
from .serializer import ImagePostSerializer, CommentSerializer
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from dotenv import load_dotenv
import logging
import uuid
import boto3
import os


load_dotenv()
def assume_role(role_arn, session_name):
    client = boto3.client(
            'sts', 
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    try:
        response = client.assume_role(
            
            RoleArn=role_arn,
            RoleSessionName=session_name
        )
        credentials = response['Credentials']
        return {
            'aws_access_key_id': credentials['AccessKeyId'],
            'aws_secret_access_key': credentials['SecretAccessKey'],
            'aws_session_token': credentials['SessionToken']
        }
    except BaseException as e:
        print(e)
def upload_image_to_s3(image, image_name, user_id,credentials):
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key'],
            aws_session_token=credentials['aws_session_token']
        )
        res = s3.put_object(
            Bucket=os.getenv('AWS_S3_BUCKET_NAME'),
            Key=f"posts/{user_id}/{image_name}",
            Body=image
        )
        return res
    except BaseException as e:
        return Response({"error": "Error uploading image to S3", 'details': e}, status=500)
    
class GuestAndAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated
    
class ImagePostAPIView(APIView):
    permission_classes = [GuestAndAuthenticated]
        
    def get(self, request, *args, **kwargs):
        image_id = kwargs.get('id')
        if image_id:
            try:
                post = ImagePost.objects.get(id=image_id)
                serializer = ImagePostSerializer(post)
                return Response(serializer.data)
            except ImagePost.DoesNotExist:
                return Response({"error": "Post not found"}, status=404)
        if kwargs.get('user_id'):
            image_posts = ImagePost.objects.filter(user=kwargs.get('user_id'))
            serializer = ImagePostSerializer(image_posts, many=True)
            return Response(serializer.data)
        image_posts = ImagePost.objects.all()
        serializer = ImagePostSerializer(image_posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        image_extension = request.FILES['image'].name.split('.')[-1]
        image_name = f"{uuid.uuid4()}.{image_extension}"
        assumed_role_credentials = assume_role(os.getenv('AWS_ROLE_ARN'), 'arba_cms_assume_role')
        res = upload_image_to_s3(request.FILES['image'],image_name, request.user.id, assumed_role_credentials)
        if res.get('ResponseMetadata').get('HTTPStatusCode') != 200:
            return Response({"error": "Error uploading image to S3"}, status=500)
        
        request.data['image'] = image_name
        request.data['user'] = request.user.id
        
        serializer = ImagePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        if request.method == 'POST':
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        image_post = ImagePost.objects.get(pk=kwargs.get('id'))
        if not image_post:
            return Response({"error": "Post not found"}, status=404)
        serializer = ImagePostSerializer(image_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        image_post = ImagePost.objects.get(pk=kwargs.get('id'))
        image_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentAPIView(APIView):
    permission_classes = [GuestAndAuthenticated]
    def get(self, request, *args, **kwargs):
        if kwargs.get('image_post_id'):
            comments = Comment.objects.filter(image_post=kwargs.get('image_post_id'))
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        request.data['image_post'] = request.data.get('image_post_id')
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logging.debug(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs.get('id'))
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs.get('id'))
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)