from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images",default="default/user.png")
    university = models.CharField(max_length=5000)
    major = models.CharField(max_length=5000)
    interests = models.CharField(max_length=5000)


class Post(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_id = models.AutoField
    post_title = models.CharField(max_length=5000)
    post_content = models.CharField(max_length=5000)
    post_topic = models.CharField(max_length=5000)
    timestamp= models.DateTimeField(default=now)
    image = models.ImageField(upload_to="images",default="")


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    reply_id = models.AutoField
    reply_content = models.CharField(max_length=5000) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default='')
    timestamp= models.DateTimeField(default=now)
    image = models.ImageField(upload_to="images",default="")


class Events(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name


class Calendar(models.Model):
    type = models.CharField(max_length=200)
    date = models.DateField()
    title = models.ForeignKey(Events, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title