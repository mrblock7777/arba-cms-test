from django.urls import path
from . import views

urlpatterns = [
    path('imagepost/', views.ImagePostAPIView.as_view()),
    path('imagepost/<int:id>/', views.ImagePostAPIView.as_view()),
    path('imagepost/user/<int:user_id>/', views.ImagePostAPIView.as_view()),
    path('comment/', views.CommentAPIView.as_view()),
    path('comment/<int:id>/', views.CommentAPIView.as_view()),
    path('imagepost/comment/<int:image_post_id>/', views.CommentAPIView.as_view())
]