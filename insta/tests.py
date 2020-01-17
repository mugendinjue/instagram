from django.test import TestCase
from . models import Image,Comment
from django.contrib.auth.models import User


class TestImages(TestCase):
  '''
  Class where we write our image models tests
  '''
  def setUp(self):
    '''
    function that runs before others
    '''
    self.test_user = User(username = 'denis')
    self.test_user.save()
    self.image = Image(image = 'denis.jpeg',name = 'denis',caption = 'denis',user = self.test_user)
    self.comments = Comment(comment = 'awesome',image = self.image,user = self.test_user)

  def test_instance(self):
    self.assertTrue(isinstance(self.image,Image))


  def test_save_image(self):
    self.image.save_image()
    image = Image.objects.all()
    self.assertTrue(len(image)>0)


  def test_delete_image(self):
    self.image2 = Image(image = 'mugendi.jpeg',name = 'mugendi',caption = 'mugendi',user = self.test_user)
    self.image2.save_image()
    self.image.save_image()
    self.image.delete_post()
    images = Image.objects.all()
    self.assertEqual(len(images),1)


  def test_search(self):
    self.image.save_image()
    self.image2 = Image(image = 'mugendi.jpeg',name = 'mugendi',caption = 'mugendi',user = self.test_user)
    self.image2.save_image()
    search_term = "e"
    search1 = Image.search_images(search_term)
    search2 = Image.objects.filter(name__icontains = search_term)
    self.assertEqual(len(search2),len(search1))


  def test_display_images(self):
    self.image.save_image()
    self.image2= Image(image = 'mugendi.jpeg',name = 'mugendi',caption = 'mugendi',user = self.test_user)
    self.image2.save_image()
    dt = Image.display_images()
    self.assertEqual(len(dt),2)





class TTestComments(TestCase):
  '''
  class that will test the profile model
  '''
  def setUp(self):
    self.test_user = User(username = 'denis')
    self.test_user.save()
    self.image = Image(image = 'denis.jpeg',name = 'denis',caption = 'denis',user = self.test_user)
    self.comments = Comment(comment = 'awesome',image = self.image,user = self.test_user)


