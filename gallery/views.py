from django.shortcuts import render

# Create your views here.
def index(request):
  '''
  View function that displays to index template
  '''
  title = 'Pinstagram - Home'

  context = {
    'title':title
  }

  return render(request, 'app_templates/index.html', context)

def register_user(request):
  '''
  view function that displays to register page,  
  '''
  title = 'Register - Pinstagram'

  context = {
    'title':title
  }

  return render(request, 'django_registration/register.html', context)

def login_user(request):
  '''
  view function that renders login template
  '''
  title = 'Login - Pinstagram'

  context = {
    'title':title
  }

  return render(request, 'django_registration/login.html', context)