from django.conf.urls import url
from django.conf.urls.static import static
from gallery import views
from django.conf import settings

urlpatterns = [
  url(r'^$', views.index, name = 'home'),
  url(r'^register_user/', views.register_user, name = 'register_user'),
  url(r'^profile/$', views.profile, name = 'profile'),
  url(r'^new_post/$', views.create_post, name = 'create_post'),
]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)