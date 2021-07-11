from django.test import TestCase
from .models import ImagePost, UserProfile, PostLikes, PostComment, user_new

# Create your tests here.
class TestImageClass(TestCase):
  '''
  Testing save, caption update and delete methods of Image post class
  '''
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

  def testdeleteimage(self):
    self.new_image.save_image()
    self.new_image.delete_image()
    images = ImagePost.objects.all()
    self.assertTrue(len(images)==0)

  def testupdatecaption(self):
    self.new_image.save_image()
    new_caption = 'Live, love, Laugh'
    ImagePost.update_caption('THis is how we do it', new_caption)
    ImagePost.objects.get(pk=1).refresh_from_db()

    self.assertTrue(new_caption == ImagePost.objects.get(image_caption = 'Live, love, Laugh').image_caption)


class TestProfileClass(TestCase):
  '''
  Testing save, udate and delete methods of UserProfile class
  '''
  #setup method
  def setUp(self):
    self.new_comment = PostComment(1,'Nice',1)
    self.new_comment.save()
    
    self.new_like = PostLikes(1,1,1)
    self.new_like.save()
    
    new_user = user_new
    new_user.save()
    
    self.new_profile = UserProfile(1,'img.png','this is bio',1)
    self.new_profile.save()

  #test instance creation
  def testinstance(self):
    self.assertTrue(isinstance(self.new_profile, UserProfile))

  def testsaveprofile(self):
    self.new_profile.save_profile()
    profiles = UserProfile.objects.all()

    self.assertEqual(len(profiles), 1)

  def testdeleteprofile(self):
    self.new_profile.save_profile()
    self.new_profile.delete_profile()

    self.assertTrue(len(UserProfile.objects.all())==0)
  