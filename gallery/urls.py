from django.conf.urls import url
from . import views

urlpattern = [
  url(r'^$', views.register_user, name = 'register_user'),
  url(r'login', views.login_user, name = 'login_user'),
  url(r'home/$', views.index, name = 'home'),
  
]