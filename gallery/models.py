from django.db import models

# Create your models here.
class UserProfile(models.Model):
  photo_path = models.ImageField(upload_to = 'gallery/')
  bio = models.CharField(200)
  