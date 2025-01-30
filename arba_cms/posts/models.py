
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ImagePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.TextField()
    caption= models.TextField()

    def __str__(self):
        return f"{self.image}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_post = models.ForeignKey(ImagePost, on_delete=models.CASCADE)
    text = models.TextField()
    
    def __str(self):
        return self.text