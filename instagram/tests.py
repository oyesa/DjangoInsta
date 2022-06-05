from django.test import TestCase
from .models import *




# Create your tests here.

#Testing Image 
class ImageTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='test_user',
            first_name='Shaybo',
            last_name='Obie'
        )
        Image.objects.create(
            image_name='test_image',
            image='https://res.cloudinary.com/oyesa/image/upload/v1654326204/profile-pics/clipart1821286_edjcgy.png',
            image_caption='test image',
            profile_id=user.id,
            user_id=user.id
        )

    def test_image_name(self):
        image = Image.objects.get(image_name='test_image')
        self.assertEqual(image.image_name, 'test_image')

#Testing Profile
class ProfileTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='test_user',
            first_name='Shaybo',
            last_name='Obie'
        )
        Profile.objects.create(
            bio='test bio',
            profile_photo='static/img/cover 11.png',
            user_id=user.id
        )

    def test_bio(self):
        profile = Profile.objects.get(bio='test bio')
        self.assertEqual(profile.bio, 'test bio')


#Testing Image_Likes
class LikesTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='test_user',
            first_name='Shaybo',
            last_name='Obie'
        )
        Profile.objects.create(
            bio='test bio',
            profile_photo='static/img/cover 11.png',
            user_id=user.id
        )
        image = Image.objects.create(
            image_caption='test post',
            image='https://res.cloudinary.com/oyesa/image/upload/v1654326204/profile-pics/clipart1821286_edjcgy.png',
            profile_id=user.id,
            user_id=user.id
        )
        Likes.objects.create(
            image_id=image.id,
            user_id=user.id
        )