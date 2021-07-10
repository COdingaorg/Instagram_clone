from django.conf.urls import url
from gallery import views

urlpatterns = [
  url(r'^$', views.register_user, name = 'register_user'),
  url(r'^login/', views.login_user, name = 'login_user'),
  url(r'home/$', views.index, name = 'home'),
  
]