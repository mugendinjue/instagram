from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as main_views

urlpatterns = [
  path('',main_views.register,name='register'),
  path('profile/',main_views.profile,name='profile'),
  path('login/',auth_views.LoginView.as_view(template_name = 'auth/login.html'),name='login'),
  path('logout/',auth_views.LogoutView.as_view(template_name = 'auth/logout.html'),name='logout'),
  path('index/',main_views.index,name='index'),
]