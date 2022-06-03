from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField



# Create your models here.
class Image(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
  image=CloudinaryField('image')
  image_name=models.CharField(max_length=200)
  image_description=models.TextField()
  image_date=models.DateTimeField(auto_now_add=True)
  profile=models.ForeignKey(User, on_delete=models.CASCADE)


  def __str__(self):
    return self.image_name