from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterNewUser(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class AddNewPost(forms.Form):
  post_image = forms.ImageField(label='upload Image')
  post_title = forms.CharField(label='Post Title :', max_length=100)
  caption = forms.Textarea()