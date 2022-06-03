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


#update profile
@login_required(login_url='/accounts/login/')
def update_profile(request):
  if request.method== 'POST':
    current_user=request.user
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    bio = request.POST['bio']
    profile_image = request.FILES['profile_pic']
    profile_image = cloudinary.uploader.upload(profile_image)
    profile_url = profile_image['url']
    user = User.objects.get(id=current_user.id)

    #check if user profile exists
    if Profile.objects.filter(user_id=current_user.id).exists():
        profile = Profile.objects.get(user_id=current_user.id)
        profile.profile_photo = profile_url
        profile.bio = bio
        profile.save()
    else:
        profile = Profile(user_id=current_user.id,profile_photo=profile_url, bio=bio)
        profile.save_profile()
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        return redirect('/profile', {'success': 'Profile Update Successful'})
  else:
      return render(request, 'profile.html', {'danger': 'Profile Update Unsuccessful'})

#profile view with current user details
def current_user_profile(request, id):
  return render(request, 'current-user-profile.html')

#image likes 
@login_required(login_url='/accounts/login/')
def image_likes(request, id):
  likes=Likes.objects.filter(image_id=id).first()
  if Likes.objects.filter(image_id=id, user_id=request.user_id).exists():
    likes.delete()
    image=Image.objects.get(id=id)
    if image.like_count==0:
      image.like_count=0
      image.save()
    else:
      image.like_count-=1
      image.save()
    return redirect('/')
  else:
    likes=Likes(image_id=id, user_id=request.user.id)
    likes.save()
    image=Image.objects.get(id=id)
    image.like_count=image.like_count +1
    image.save()
    return redirect('/')