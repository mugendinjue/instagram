from django.shortcuts import render
from django.http import Http404

def register(request):
  return render(request,'auth/registration.html')

def login(request):
  return render(request,'auth/login.html')


def index(request):
  return render (request,'main/index.html')
