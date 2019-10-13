from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import Registration,UpdateUser,UpdateProfile,CommentForm
from django.contrib.auth.decorators import login_required
from .models import Image
from django.http import JsonResponse


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
  comment_form = CommentForm()
  images = Image.display_images()
  return render (request,'main/index.html',{"images":images,"comment_form":comment_form})

@login_required
def update_profile(request):
  if request.method == 'POST':
    u_form = UpdateUser(request.POST,instance=request.user)
    p_form = UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('profile')
  else:
    u_form = UpdateUser(instance=request.user)
    p_form = UpdateProfile(instance=request.user.profile) 
  params = {
    'u_form':u_form,
    'p_form':p_form
  }
  return render(request,'auth/update_profile.html',params)

@login_required
def commenting(request,image_id):
  c_form = CommentForm()
  image = Image.objects.filter(pk = image_id).first()
  if request.method == 'POST':
    c_form = CommentForm(request.POST)
    if c_form.is_valid():
      comment = c_form.save(commit = False)
      comment.user = request.user
      comment.image = image
      comment.save() 
  return redirect('index')

@login_required
def likes(request,image_id):
  image = Image.objects.filter(pk = image_id).first()
  return JsonResponse(image.all_likes,safe=False)


@login_required
def allcomments(request,image_id):
  image = Image.objects.filter(pk = image_id).first()
  return render(request,'main/imagecomments.html',{"image":image})