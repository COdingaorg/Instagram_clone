from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import RegisterNewUser,AddNewPost, UpdateProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, User

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
  current_user_id = request.user.id

  
  try:
      user_profile = UserProfile.objects.filter(user = current_user_id).order_by('id').first()
  except UserProfile.DoesNotExist:
    user_profile = None
  context = {
    'user_profile':user_profile,
    'title':title
  }
  return render(request, 'app_templates/index.html', context)

@login_required(login_url='login')
def profile(request):
  '''
  view function that renders profile template data
  '''
  title = 'profile - Pinstagram'
  if request.method == 'POST':
    form = UpdateProfile(request.POST, request.FILES)
    if form.is_valid():
      photo = form.cleaned_data['photo']
      bio = form.cleaned_data['bio']
      user_id = request.user.id
      new_profile = UserProfile(photo_path = photo, bio = bio, user_id = user_id)
      new_profile.save_profile()

      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else:
    current_user_id = request.user.id
    try:
      user_profile = UserProfile.objects.filter(user = current_user_id).order_by('id').first()
    except UserProfile.DoesNotExist:
      user_profile = None
    form = UpdateProfile
    context = {
      'user_profile':user_profile,
      'form':form,
      'title':title,
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
        return redirect('profile', {'info':info, 'path':path})
      
      else:
        new_post.profile = userprofile
        new_post.save()

        try:
          return redirect('home')
        except:
          return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         
  else:
    form = AddNewPost
    context = {
      'form':form,
      'title':title,
      }
    return render(request, 'app_templates/new_post.html', context)

def search_user(request):
  title = 'search Results'

  if 'search_term' in request.GET and request.GET['search_term']:
    search_term = request.GET.get('search_term')

    users = User.objects.filter(username = search_term)
    context = {
      'users':users,
      'title':title,

    }

    return render(request, 'app_templates/search_user.html', context)
  else:
    message = 'No users Found'
    return render(request, 'app_templates/search_user.html', {'messeage':message})