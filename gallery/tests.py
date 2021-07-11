from django.test import TestCase
from .models import ImagePost, UserProfile, PostLikes, PostComment, user_new
from django.contrib.auth.models import User

# Create your tests here.
class TestImageClass(TestCase):
  def setUp(self):
    #create instance
    self.new_comment = PostComment(1,'Nice',1)
    self.new_comment.save()
    
    self.new_like = PostLikes(1,1,1)
    self.new_like.save()
    
    new_user = user_new
    new_user.save()
    
    self.new_profile = UserProfile(1,'img.png','this is bio',1)
    self.new_profile.save()

    self.new_image = ImagePost(1,'image.png', 'Alphabet', 'THis is how we do it', 1 ,1, 1)

    #test instance 
  def testInstance(self):
    self.assertTrue(isinstance(self.new_image, ImagePost))

  def testsaveimage(self):
    self.new_image.save_image()
    images = ImagePost.objects.all()
    self.assertTrue(len(images)>0)
