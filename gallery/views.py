from django.shortcuts import redirect, render
from .forms import RegisterNewUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
  title = f'{request.user.id} profile - Pinstagram'

  context = {
    'title':title
  }

  return render(request, 'registration/profile.html', context)

