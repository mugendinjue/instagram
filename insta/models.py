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

  @property
  def all_comments(self):
    return self.comments.all()

  @property
  def all_likes(self):
    return self.imagelikes.count()    

  def __str__(self):
    return "%s image" % self.name

class Like(models.Model):
  like = models.BooleanField()
  image = models.ForeignKey(Image, on_delete = models.CASCADE,related_name='imagelikes')
  user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='userlikes')

  def __str__(self):
    return "%s like" % self.image

class Comment(models.Model):
  comment = models.TextField()
  image = models.ForeignKey(Image,on_delete = models.CASCADE,related_name='comments')
  user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='comments')

  @classmethod
  def display_comments_by_imageId(cls,image_id):
    comments = cls.objects.filter(image_id = image_id)
    return comments

  def __str__(self):
    return "%s comment" % self.image

class Profile(models.Model):
  profile_pic = models.ImageField(default='default.jpg',upload_to='profile/')
  bio = models.TextField()
  user = models.OneToOneField(User,on_delete = models.CASCADE)


  @receiver(post_save , sender = User)
  def create_profile(instance,sender,created,**kwargs):
    if created:
      Profile.objects.create(user = instance)

  @receiver(post_save,sender = User)
  def save_profile(sender,instance,**kwargs):
    instance.profile.save()

  @property
  def all_followers(self):
    return self.followers.count()   

  @property
  def all_following(self):
    return self.following.count()  


  def __str__(self):
    return "%s profile" % self.user

class Follows(models.Model):
  follower = models.ForeignKey(Profile, related_name='following',on_delete = models.CASCADE)
  followee = models.ForeignKey(Profile, related_name='followers',on_delete = models.CASCADE)

