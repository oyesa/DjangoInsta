from django.shortcuts import render, redirect
from django.http  import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import * 
from django.urls import reverse
from django.core import exceptions
import cloudinary
import cloudinary.uploader
import cloudinary.api


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
@login_required(login_url='/accounts/login/')
def current_user_profile(request, id):
  if User.objects.filter(id=id).exists():
    user=User.objects.get(id=id)
    images=Image.objects.filter(user_id=id)
    profile=Profile.objects.filter(user_id=id).first()
    return render(request, 'current-user-profile.html', {'user':user, 'images':images, 'profile':profile})
  else:
    return redirect('/')


#image likes 
@login_required(login_url='/accounts/login/')
def image_likes(request, id):
  likes=Likes.objects.filter(image_id=id).first()
  if Likes.objects.filter(image_id=id, user_id=request.user.id).exists():
    likes.delete()
    image=Image.objects.get(id=id)
    if image.likes_count==0:
       image.likes_count= 0
       image.save()
    else:
       image.likes_count -= 1
       image.save()
    return redirect('/')
  else:
     likes=Likes(image_id=id, user_id=request.user.id)
     likes.save()
     image=Image.objects.get(id=id)
     image.likes_count = image.likes_count +1
     image.save()
     return redirect('/')

#search images
@login_required(login_url='/accounts/login/')
def search_images(request):
    if 'search' in request.GET and request.GET['search']:
        search_term=request.GET.get('search').lower()
        images=Image.search_by_image_name(search_term)
        message=f'{search_term}'
        title=message
        return render(request, 'search.html', {'success': message, 'images': images})
    else:
        message = 'Type for search term'
        return render(request, 'search.html', {'danger': message})

#save image details to cloudinary
@login_required(login_url='/accounts/login/')
def save_image(request):
  if request.method== 'POST':
    image_name=request.POST['image_name']
    image_caption=request.POST['image_caption']
    image_file=request.FILES['image_file']
    image_file=cloudinary.uploader.upload(image_file)
    image_url=image_file['url']
    image_public_id=image_file['public_id']
    image=Image(image_name=image_name, image_caption=image_caption, image=image_url,profile_id=request.POST['user_id'], user_id=request.POST['user_id'])
    image.save_image()
    return redirect('/profile', {'success': 'Image Upload Successful'})
  else:
    return render(request, 'profile.html', {'danger': 'Image Not Uploaded'})


#single image view
@login_required(login_url='/accounts/login/')
def single_image(request, id):
  image=Image.objects.get(id=id)
  related_images=Image.objects.filter(user_id=image.user_id).order_by('-image_date')
  title=image.image_name
  if Image.objects.filter(id=id).exists():
    comments=Comments.objects.filter(image_id=id)
    return render(request, 'image.html', {'image': image, 'comments': comments, 'images': related_images, 'title': title})
  else:
    return redirect('/')

#save comments
@login_required(login_url='/accounts/login/')
def save_comment(request):
    if request.method== 'POST':
        comment=request.POST['comment']
        image_id=request.POST['image_id']
        image=Image.objects.get(id=image_id)
        user=request.user
        comment=Comments(comment=comment, image_id=image_id, user_id=user.id)
        comment.save_comment()
        image.comment_count=image.comment_count + 1
        image.save()
        return redirect('/picture/' + str(image_id))
    else:
        return redirect('/')