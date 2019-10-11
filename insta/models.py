from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
  image = models.ImageField(upload_to='instaimages/')
  name = models.CharField(max_length=60)
  caption = models.TextField()
  user = models.ForeignKey(User,on_delete = models.CASCADE)

  def __str__(self):
    return "%s the place" % self.name

class Like(models.Model):
  like = models.BooleanField()
  image = models.ForeignKey(Image, on_delete = models.CASCADE)

  def __str__(self):
    return "%s the place" % self.image

class Comment(models.Model):
  comment = models.TextField()
  image = models.ForeignKey(Image,on_delete = models.CASCADE)

  def __str__(self):
    return "%s the place" % self.image

class Profile(models.Model):
  profile_pic = models.ImageField(upload_to='profile/')
  bio = models.TextField()
  user = models.OneToOneField(User,on_delete = models.CASCADE)


  def __str__(self):
    return "%s the place" % self.user