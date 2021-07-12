from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import RegisterNewUser,AddNewPost, UpdateProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ImagePost, PostComment, PostLikes, UserProfile, User
import datetime as dt

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
  displays posts
  displays user profile details
  renders suggestions
  '''
  title = 'Pinstagram - Home'
  current_user_id = request.user.id

  
  try:
    user_profile = UserProfile.objects.filter(user = current_user_id).order_by('id').first()
  except UserProfile.DoesNotExist:
    user_profile = None

  #collecting posts
  try:
    all_posts = ImagePost.objects.all()
    message = 'success'
  except ImagePost.DoesNotExist:
    all_posts = None
    message = 'Try failed'

  #returning number of user profile
  try:
    suggestions = UserProfile.objects.all()[1:9]
    message = 'success'
  except ImagePost.DoesNotExist:
    suggestions = None
    message = 'Try failed'

  #returning number of likes and comments
  post_id = 5
  try:
    likes = PostLikes.objects.filter(post=post_id)
  except PostLikes.DoesNotExist:
    likes = None
  #eturning comments count
  try:
    comments = PostComment.objects.filter(post=post_id)
    top_comment = comments.first()
  except PostComment.DoesNotExist:
    comments = None

  

  
  
  context = {
    'top_comment':top_comment,
    'likes':likes,
    'comments':comments,
    'suggestions':suggestions,
    'all_posts':all_posts,
    'user_profile':user_profile,
    'title':title,
    'message':message,
  }
  return render(request, 'app_templates/index.html', context)

#view function rendering to profile template
@login_required(login_url='login')
def profile(request):
  '''
  view function that renders profile template data
  displays current user profile data
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
      def get_user_profile():
        try:
          userprofile = UserProfile.objects.get(user = current_user_id)
        except UserProfile.DoesNotExist:
          userprofile = None
        
        return userprofile

      userprofile = get_user_profile()
      if not userprofile:
        path = request.path
        messages.warning(request,'Your Profile is Empty. Create one to proceed')

        context = {
          'path':path,
        }
        return HttpResponseRedirect('/profile', context)
      
      else:
        new_post.profile = userprofile
        new_post.date_created = dt.datetime.now()
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

    users = User.objects.filter(username__icontains = search_term)
    context = {
      'search_term':search_term,
      'users':users,
      'title':title,

    }

    return render(request, 'app_templates/search_user.html', context)
  else:
    message = 'No users Found'
    return render(request, 'app_templates/search_user.html', {'messeage':message})

#adds comment to posts
def add_comment(request):
  title = 'Add comment'
  if request.method == 'POST':
    comment = request.POST.get('comment')
    post_id = request.POST.get('post_id')
    user = User.objects.get(id = request.user.id)
    post = ImagePost.objects.get(id = post_id)
    date_created = dt.datetime.now()

    new_comment = PostComment(comments = comment, date_created = date_created, user_commenter = user, post = post )
    new_comment.save()

    return render(request, 'app_templates/index.html')

  else:
    return render(request, 'app_templates/index.html', locals())

#adds like function    
def add_like(request):
  '''
  view function that collect like form values and creates a like
  '''
  if request.method == 'POST':
    imagepost = ImagePost.objects.get(id = request.POST.get('post_like'))
    date_created = dt.datetime.now()
    user_like = User.objects.get(id = request.user.id)
    
    new_like = PostLikes(user_liker = user_like, date_created = date_created, post = imagepost)
    new_like.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  else:
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))