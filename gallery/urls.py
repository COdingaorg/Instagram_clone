from django.conf.urls import url
from gallery import views

urlpatterns = [
  url(r'^$', views.index, name = 'home'),
  
  
]