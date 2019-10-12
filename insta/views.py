from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import Registration
from django.contrib.auth.decorators import login_required
from .models import Image


def register(request):
  if request.method == 'POST':
    form = Registration(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request,f'Account for {username} created,tou can now login')
      return redirect('login')
  else:
    form = Registration()
  return render(request,'auth/registration.html',{"form":form})


@login_required
def profile(request):
  current_user = request.user
  images = Image.objects.filter(user_id = current_user.id).all()
  return render(request,'auth/profile.html',{"images":images})

@login_required
def index(request):
  images = Image.display_images()
  print(images)
  return render (request,'main/index.html',{"images":images})
