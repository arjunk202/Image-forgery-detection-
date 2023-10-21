from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userProfile(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='profile_pic',default='sherlock.jpg')
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=5000)
    
    
    def __str__(self):
        return self.user.username + " profile"



class ifd(models.Model):

    
    
    image = models.ImageField(upload_to='images',default='sherlock.jpg')
    
    
    
    def __str__(self):
        return "image"