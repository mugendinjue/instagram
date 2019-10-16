from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import Registration,UpdateUser,UpdateProfile,CommentForm,postImageForm
from django.contrib.auth.decorators import login_required
from .models import Image,Profile,Like,Follows
from django.http import JsonResponse
from django.contrib.auth.models import User
from .email import send_welcome_email


def register(request):
  if request.method == 'POST':
    form = Registration(request.POST)
    if form.is_valid():
      form.save()
      email = form.cleaned_data['email']
      username = form.cleaned_data.get('username')

      messages.success(request,f'Account for {username} created,you can now login')
      return redirect('login')
  else:
    form = Registration()
  return render(request,'auth/registration.html',{"form":form})


@login_required
def profile(request):
  current_user = request.user
  images = Image.objects.filter(user_id = current_user.id).all()
  
  return render(request,'auth/profile.html',{"images":images,"current_user":current_user})

@login_required
def index(request):
  comment_form = CommentForm()
  post_form = postImageForm()
  images = Image.display_images()
  users = User.objects.all()
  
  return render (request,'main/index.html',{"images":images,"comment_form":comment_form,"post":post_form,"all":users})

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
  if request.method == 'GET':
    image = Image.objects.get(pk = image_id)
    user = request.user
    check_user = Like.objects.filter(user = user,image = image).first()
    if check_user == None:
      image = Image.objects.get(pk = image_id)
      like = Like(like = True,image = image,user = user)
      like.save()
      return JsonResponse({'success':True,"img":image_id,"status":True})
    else:
      check_user.delete()
      return JsonResponse({'success':True,"img":image_id,"status":False})
 


@login_required
def allcomments(request,image_id):
  image = Image.objects.filter(pk = image_id).first()
  return render(request,'main/imagecomments.html',{"image":image})


@login_required
def search(request):
  if 'search_user' in request.GET and request.GET["search_user"]:
    name = request.GET.get('search_user')
    the_users = Profile.search_profiles(name)
    images = Image.search_images(name)
    print(the_users) 
    return render(request,'main/search.html',{"users":the_users,"images":images})
  else:
    return render(request,'main/search.html')


@login_required
def post(request):
  if request.method == 'POST':
    post_form = postImageForm(request.POST,request.FILES) 
    if post_form.is_valid():
      the_post = post_form.save(commit = False)
      the_post.user = request.user
      the_post.save()
  return redirect('index')

@login_required
def others_profile(request,pk):
  user = User.objects.get(pk = pk)
  images = Image.objects.filter(user = user)
  c_user = request.user
  
  return render(request,'main/othersprofile.html',{"user":user,"images":images,"c_user":c_user})

@login_required
def follow(request,user_id):
  followee = request.user
  followed = Follows.objects.get(pk=user_id)
  follow_data = Follows(follower = followee.profile,followee = followed.profile)
  follow_data.save()
  return redirect('others_profile')

@login_required
def unfollow(request,user_id):
  followee = request.user
  follower = Follows.objects.get(pk=user_id)
  follow_data = Follows.objects.filter(follower = follower,followee = followee).first()
  follow_data.delete()
  return redirect('others_profile')

@login_required
def delete(request,image_id):
  image = Image.objects.get(pk=image_id)
  if image:
    image.delete_post()
  return redirect('profile')




@login_required
def deleteaccount(request):
  
  current_user = request.user
  account = User.objects.get(pk=current_user.id)
  account.delete()
  return redirect('register')

