from django.shortcuts import render, redirect
from django.http  import HttpResponse



# Create your views here.

def home(request):
  return render(request, 'home.html')


#profile view
def profile(request):
  return render(request, 'profile.html')

def update_profile(request):
  return render(request, 'profile.html')

#profile view with current user details
def current_user_profile(request, id):
  return render(request, 'current-user-profile.html')

#image likes 
def image_likes(request, id):
  return redirect('/')