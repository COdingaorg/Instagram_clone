from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from tinymce.models import HTMLField

# Create your models here.
class FollowChain(models.Model):
  follow = models.ForeignKey(User, on_delete=CASCADE)

class Follower(models.Model):
  followers = models.ForeignKey(User, on_delete=CASCADE)

class UserProfile(models.Model):
  photo_path = models.ImageField(upload_to = 'gallery/')
  bio = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=CASCADE)
  follows = models.ForeignKey(FollowChain, on_delete=CASCADE,null=True, blank=True)
  followers = models.ForeignKey(Follower, on_delete=CASCADE,null=True, blank=True)

  def save_profile(self):
    self.save()

  def delete_profile(self):
    self.delete()

  @classmethod
  def update_bio(cls, id, new_bio):
    to_update = cls.objects.filter(pk = id).update(bio = new_bio)

class PostLikes(models.Model):
  likes = models.IntegerField(auto_created=True)
  user_liker = models.ForeignKey(User, on_delete=CASCADE)

class PostComment(models.Model):
  comments = models.CharField(max_length = 260)
  user_commenter = models.ForeignKey(User, on_delete=CASCADE)

class ImagePost(models.Model):
  image = models.ImageField(upload_to = 'posts/')
  image_name = models.CharField(max_length=100)
  image_caption = HTMLField()
  profile = models.ForeignKey(UserProfile, on_delete=CASCADE)
  likes = models.ForeignKey(PostLikes, on_delete=CASCADE,null=True, blank=True)
  comments = models.ForeignKey(PostComment, on_delete=CASCADE,null=True, blank=True)

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
