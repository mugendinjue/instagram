from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Image(models.Model):
  image = models.ImageField(upload_to='instaimages/')
  name = models.CharField(max_length=60)
  caption = models.TextField()
  user = models.ForeignKey(User,on_delete = models.CASCADE)

  @classmethod
  def display_images(cls):
    images = cls.objects.all()
    return images

  def __str__(self):
    return "%s image" % self.name

class Like(models.Model):
  like = models.BooleanField()
  image = models.ForeignKey(Image, on_delete = models.CASCADE)

  def __str__(self):
    return "%s like" % self.image

class Comment(models.Model):
  comment = models.TextField()
  image = models.ForeignKey(Image,on_delete = models.CASCADE)

  def __str__(self):
    return "%s comment" % self.image

class Profile(models.Model):
  profile_pic = models.ImageField(upload_to='profile/',default='profile/default.jpeg')
  bio = models.TextField()
  user = models.OneToOneField(User,on_delete = models.CASCADE)


  @receiver(post_save , sender = User)
  def create_profile(instance,sender,created,**kwargs):
    if created:
      Profile.objects.create(user = instance)

  @receiver(post_save,sender = User)
  def save_profile(sender,instance,**kwargs):
    instance.profile.save()


  def __str__(self):
    return "%s profile" % self.user