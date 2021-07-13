from django.conf.urls import url
from django.conf.urls.static import static
from gallery import views
from django.conf import settings

urlpatterns = [
  url(r'^$', views.index, name = 'home'),
  url(r'^register_user/', views.register_user, name = 'register_user'),
  url(r'^profile/$', views.profile, name = 'profile'),
  url(r'^new_post/$', views.create_post, name = 'create_post'),
  url(r'^search_user/$', views.search_user, name='search_user'),
  url(r'^add_comment/$', views.add_comment, name = 'add_comment'),
  url(r'^post/like/', views.add_like, name = 'like post'),
  url(r'^post/(\d+)$', views.open_post, name = 'open_post'),
  url(r'^follow/', views.follow_followed, name = 'follow_followed')
]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)