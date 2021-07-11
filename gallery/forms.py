from gallery.models import ImagePost, UserProfile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from tinymce.models import HTMLField

class RegisterNewUser(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class AddNewPost(forms.ModelForm):
  class Meta:
    model = ImagePost
    exclude = ['profile', 'likes', 'comments']
    fields = ['image', 'image_name', 'image_caption']

class UpdateProfile(forms.Form):
  photo = forms.ImageField()
  bio = forms.CharField(max_length=200)
  