import os
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.permissions import BasePermission, IsAuthenticated
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# Create your views here.
class UserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated
    
class UserView(APIView):
    permission_classes = [UserOrReadOnly]
    def get(self, request, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'date_joined': user.date_joined
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, user_id):
        try:
            if(user_id != request.user.id):
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(id=user_id)
            user.username = request.data.get('username', user.username) or user.username
            user.first_name = request.data.get('first_name', user.first_name) or user.first_name
            user.last_name = request.data.get('last_name', user.last_name) or user.last_name
            user.email = request.data.get('email', user.email) or user.email
            user.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        date_joined = datetime.now()
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, date_joined=date_joined, is_active=True, is_superuser=False, is_staff=False)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            refreshToken = RefreshToken.for_user(user)
            return JsonResponse({'message': 'Login successful', 'refreshToken': str(refreshToken), 'accessToken': str(refreshToken.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)