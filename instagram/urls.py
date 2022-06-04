from . import views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns =[
  path('', views.home, name='home'),
  path('profile/', views.profile, name='profile'),
  path('profile/update/', views.profile, name='profile'),
  path('user/<int:id>/', views.current_user_profile, name='user.profile'),
  path('like/<int:id>/', views.image_likes, name='image.likes'),
  path('comment/add', views.save_comment, name='comment.add'),
  path('upload/add/', views.save_image, name='save.image'),
  path('search/', views.search_images, name='search.images'),
  path('images/<int:id>/', views.single_image, name='single.image')
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)