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

  #save, delete methods
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