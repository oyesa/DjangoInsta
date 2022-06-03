from django.shortcuts import render, redirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import * 
import cloudinary


# Create your views here.

#view for all images in the db  
@login_required(login_url='/accounts/login/')
def home(request):
  images=Image.objects.all().order_by('image_date')
  return render(request, 'home.html', {'images':images})


#profile view
@login_required(login_url='/accounts/login/')
def profile(request):
  #get profile for logged-in user
  current_user=request.user  
  images=Image.objects.filter(user_id=current_user.id)
  profile=Profile.objects.filter(user_id=current_user.id).first()
  return render(request, 'profile.html', {'images':images, 'profile':profile})

def update_profile(request):
  return render(request, 'profile.html')

#profile view with current user details
def current_user_profile(request, id):
  return render(request, 'current-user-profile.html')

#image likes 
def image_likes(request, id):
  return redirect('/')