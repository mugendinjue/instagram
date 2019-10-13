from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from . import views as main_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',main_views.register,name='register'),
  path('profile/',main_views.profile,name='profile'),
  path('login/',auth_views.LoginView.as_view(template_name = 'auth/login.html'),name='login'),
  path('logout/',auth_views.LogoutView.as_view(template_name = 'auth/logout.html'),name='logout'),
  path('index/',main_views.index,name='index'),
  path('update/',main_views.update_profile,name='update_profile'),
  re_path(r'^comment/(?P<image_id>\d+)$',main_views.commenting,name='commenting'),
  re_path(r'^likes/(?P<image_id>\d+)$',main_views.likes,name='likes'),
  re_path(r'^allcomments/(?P<image_id>\d+)$',main_views.allcomments,name='allcomments')
]

if settings.DEBUG:
  urlpatterns+= static(
    settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
  )