from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(Followers)