from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField



# Create your models here.
class Image(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
  image=CloudinaryField('image')
  image_name=models.CharField(max_length=200)
  image_caption=models.TextField()
  image_date=models.DateTimeField(auto_now_add=True)
  profile=models.ForeignKey(User, on_delete=models.CASCADE)
  likes_count=models.IntegerField(default=0)
  comment_count=models.IntegerField(default=0)

  #save, update, delete methods
  def save_image(self):
    self.save()

  def delete_image(self):
    self.delete()

  def update_caption(self, new_caption):
    self.image_caption=new_caption
    self.save()

  #classmethods
  @classmethod
  def get_images_by_user(cls, user):
    images=cls.objects.filter(user=user)
    return images

  @classmethod
  def get_single_image(cls, id):
    image=cls.objects.get(id=id)
    return image

  @classmethod
  def search_by_image(cls, search_term):
    images=cls.objects.filter(image_name_icontains=search_term)
    return images


  def __str__(self):
    return self.image_name



#Profile Model
class Profile(models.Model):
  user=models.OneToOneField(User, on_delete=models.CASCADE)
  profile_photo=CloudinaryField('image')
  bio=models.TextField(max_length=900, blank=True, null=True)

   #save, update, delete methods
  def save_profile(self):
     self.save()

  def update_profile(self):
    self.save()

  def delete_profile(self):
    self.delete()

  @classmethod
  def get_user_profile(cls, user):
    profile=cls.objects.filter(user=user)
    return profile

  def __str__(self):
    return self.user.username


#Likes Model
class Likes(models.Model):
  image=models.ForeignKey(Image, on_delete=models.CASCADE)
  user=models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.likes

#Comments Model
class Comments(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  image = models.ForeignKey(Image, on_delete=models.CASCADE)
  comment = models.CharField(max_length=200)

  def save_comment(self):
      self.save()

  def __str__(self):
    return self.comment

#Followers Model
class Followers(models.Model):
  follower = models.CharField(max_length=100)
  user = models.CharField(max_length=100)

  def __str__(self):
        return self.user


