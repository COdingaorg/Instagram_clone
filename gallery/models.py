from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from tinymce.models import HTMLField
import datetime as dt

# Create your models here.
class FollowChain(models.Model):
  follow = models.ForeignKey(User, on_delete=CASCADE)
  date_created = models.DateTimeField(default=dt.datetime.now(), editable=False, blank=True)

class Follower(models.Model):
  followers = models.ForeignKey(User, on_delete=CASCADE)
  date_created = models.DateTimeField(default=dt.datetime.now(), editable=False, blank=True)

class UserProfile(models.Model):
  photo_path = models.ImageField(upload_to = 'gallery/')
  bio = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=CASCADE)
  follows = models.ForeignKey(FollowChain, on_delete=CASCADE,null=True, blank=True)
  followers = models.ForeignKey(Follower, on_delete=CASCADE,null=True, blank=True)
  date_created = models.DateTimeField(default=dt.datetime.now(), editable=False, blank=True)

  def save_profile(self):
    self.save()

  def delete_profile(self):
    self.delete()

  @classmethod
  def update_bio(cls, id, new_bio):
    to_update = cls.objects.filter(pk = id).update(bio = new_bio)
    return to_update

class ImagePost(models.Model):
  image = models.ImageField(upload_to = 'posts/')
  image_name = models.CharField(max_length=100)
  image_caption = HTMLField()
  date_created = models.DateTimeField(editable=False, blank=True)
  profile = models.ForeignKey(UserProfile, on_delete=CASCADE)
  class Meta:
    ordering = ['-id']

  def save_image(self):
    self.save() 

  def delete_image(self):
    self.delete()

  @classmethod
  def update_caption(cls, id, new_caption):
    to_update = cls.objects.filter(pk = id)
    to_update.update(image_caption = new_caption)

  def __str__(self):
      return self 

#imported user instance for testing 
user_new = User.objects.get(pk = 1)

class PostLikes(models.Model):
  likes = models.IntegerField(auto_created=True)
  user_liker = models.ForeignKey(User, on_delete=CASCADE)
  date_created = models.DateTimeField(default=dt.datetime.now(), editable=False, blank=True)
  post = models.ForeignKey(ImagePost, on_delete=CASCADE,null=True, blank=True)
  class Meta:
    ordering = ['-id']

class PostComment(models.Model):
  comments = models.CharField(max_length = 260)
  user_commenter = models.ForeignKey(User, on_delete=CASCADE)
  date_created = models.DateTimeField(default=dt.datetime.now(), editable=False, blank=True)
  post = models.ForeignKey(ImagePost, on_delete=CASCADE,null=True, blank=True)
  class Meta:
    ordering = ['-id']
