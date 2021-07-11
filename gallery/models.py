from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, SET_NULL

# Create your models here.
class UserProfile(models.Model):
  photo_path = models.ImageField(upload_to = 'gallery/')
  bio = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=CASCADE)

class ImagePost(models.Model):
  image = models.ImageField(upload_to = 'posts/')
  image_name = models.CharField(max_length=100)
  image_caption = models.TextField(max_length=250)
  profile = models.ForeignKey(UserProfile, on_delete=CASCADE)
