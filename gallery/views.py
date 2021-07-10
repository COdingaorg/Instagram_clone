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

  return render(request, 'index.html', context)

def register_user(request):

  pass

def login_user(request):

  pass