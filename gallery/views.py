from os import sendfile
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django_heroku.core import settings
from .forms import RegisterNewUser,AddNewPost, UpdateProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FollowChain, Follower, ImagePost, PostComment, PostLikes, UserProfile, User
import datetime as dt
from .emails import send_new_user_email


# Create your views here.
#register user view function
def register_user(request):
  '''
  view function that displays to register page,  
  sends email to user
  redirects to login
  '''
  title = 'Register - Pinstagram'
  if request.method == 'POST':
    form = RegisterNewUser(request.POST)
    if form.is_valid():
      uname = form.cleaned_data['username']
      uemail = form.cleaned_data['email']
      form.save()
      send_new_user_email(uname , uemail)
      messages.success(request, 'Account Created Successfully!. Check out our Email later :)')

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
  post_id = 5 #change to a variable
  try:
    likes = PostLikes.objects.filter(post=post_id)
  except PostLikes.DoesNotExist:
    likes = None
  #eturning comments count
  try:
    comments = PostComment.objects.filter(post=post_id)
    top_comment = PostComment.objects.filter(post=post_id).first()
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
  displays posts created by user
  shows followers count and followings
  '''
  userid = request.user.id
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
    current_user_id = userid
    try:
      user_profile = UserProfile.objects.filter(user = current_user_id).order_by('id').first()
    except UserProfile.DoesNotExist:
      user_profile = None
      message = 'This user has no profile'
      raise Http404('It Failed here')

    try:
      user_prof_id = UserProfile.objects.get(user=userid).id
      user_posts = ImagePost.objects.filter(profile = user_prof_id)
    except ImagePost.DoesNotExist:
      user_posts = None
      raise Http404('Now it stopped here')

    try:

      followings = FollowChain.objects.filter(user_profile=user_prof_id)
    except ImagePost.DoesNotExist:
      followings = None

    try:
      
      followers = Follower.objects.filter(user_profile=user_prof_id)
    except ImagePost.DoesNotExist:
      followers = None

    

    form = UpdateProfile
    context = {
      'followers':followers,
      'followings':followings,
      'user_posts':user_posts,
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

        messages.success(request, 'Post Created successfully')

        try:
          return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
          return redirect('home')
         
  else:
    form = AddNewPost
    context = {
      
      'form':form,
      'title':title,
      }
    return render(request, 'app_templates/new_post.html', context)

@login_required(login_url='login')
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
@login_required(login_url='login')
def add_comment(request):
  if request.method == 'POST':
    comment = request.POST.get('comment')
    post_id = request.POST.get('post_id')
    user = User.objects.get(id = request.user.id)
    post = ImagePost.objects.get(id = post_id)
    date_created = dt.datetime.now()

    new_comment = PostComment(comments = comment, date_created = date_created, user_commenter = user, post = post )
    new_comment.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  else:
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#adds like function   
@login_required(login_url='login') 
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

#view function opening an image
@login_required(login_url='login')
def open_post(request, sentid):
  '''
  view function rendering to image page
  '''
  postid = sentid
  title = f'{request.user.username}\'s post'

  try:
    user_profile = UserProfile.objects.filter(user = request.user.id).order_by('id').first()
  except UserProfile.DoesNotExist:
    user_profile = None

  #collecting the post
  try:
    post = ImagePost.objects.get(id = postid)
    message = 'success'
  except ImagePost.DoesNotExist:
    post= None
    message = 'Try failed'

  #returning number of likes and comments
  try:
    likes = PostLikes.objects.filter(post=postid)
  except PostLikes.DoesNotExist:
    likes = None
    
  #eturning comments count
  try:
    comments = PostComment.objects.filter(post=postid)
    top_comment = comments.first()
  except PostComment.DoesNotExist:
    comments = None

  context = {
    'top_comment':top_comment,
    'likes':likes,
    'comments':comments,
    'post':post,
    'user_profile':user_profile,
    'title':title,
    'message':message}

  return render(request, 'app_templates/image_post.html', context)

#adds a following and follow capability
@login_required(login_url='login')
def follow_followed(request):
  '''
  view function that enables following and follows
  '''
  user_id = request.user.id
  if request.method == 'POST':
    user = User.objects.get(id = user_id)
    stranger_id= request.POST.get('strangeid')
    stranger = User.objects.get(id = stranger_id)
    user_profile = UserProfile.objects.get(user = user_id)
    stranger_profile = UserProfile.objects.get(user = stranger_id)

    #user is following the stranger hence its a user's following
    follow = FollowChain(follow = stranger, user_profile = user_profile)
    #user following a stranger is a strangers follower
    follower = Follower(followers = user, user_profile = stranger_profile)

    follow.save()
    follower.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  else:
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
