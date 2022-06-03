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