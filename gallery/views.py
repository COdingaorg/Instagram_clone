from django.core import exceptions
from django.shortcuts import redirect, render
from .forms import RegisterNewUser,AddNewPost
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile

# Create your views here.
#register user view function
def register_user(request):
  '''
  view function that displays to register page,  
  '''
  title = 'Register - Pinstagram'
  if request.method == 'POST':
    form = RegisterNewUser(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Account Created Successfully!')
      return redirect('login')
  else:
    form = RegisterNewUser
  context = {
    'title':title,
    'form':form,
  }
  return render(request, 'django_registration/registration_form.html', context)

#index view function
@login_required(login_url=('login'))
def index(request):
  '''
  View function that displays to index template
  '''
  title = 'Pinstagram - Home'
  context = {
    'title':title
  }
  return render(request, 'app_templates/index.html', context)

@login_required(login_url='login')
def profile(request):
  '''
  view function that renders profile template data
  '''
  title = f'{request.user.username} profile - Pinstagram'

  context = {
    'title':title
  }

  return render(request, 'registration/profile.html', context)

@login_required(login_url='login')
def create_post(request):
  current_user_id = request.user.id
  title = 'create Post'
  
  if request.method == 'POST':
    form = AddNewPost(request.POST, request.FILES)
    if form.is_valid():
      new_post = form.save(commit=False)

      #find if a user has a profile, then attach post to it ,
      # else prompt to create one, then save the details
      try:
        userprofile = UserProfile.objects.get(user = current_user_id)
      except UserProfile.DoesNotExist:
        userprofile = 'empty'

      if userprofile == 'empty':
        path = request.path
        info = messages.error(request, 'Your Profile is Empty. Create one to proceed')
        return redirect('update_profile', {'info':info, 'path':path})
      
      else:
        new_post.profile = userprofile
        new_post.save()

      return redirect('home')
  else:
    form = AddNewPost
    context = {
      'form':form,
      'title':title,
      }
    return render(request, 'app_templates/new_post.html', context)

@login_required(login_url='login')
def update_profile(request):
  title = 'Update Profile'
  form = ''

  context = {
    'title':title,
    'form' : form,
  }

  return render(request, 'app_templates/update_profile.html')
