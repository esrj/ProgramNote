from django.db import models
from django.contrib.auth.models import AbstractUser
from ProgramNote import settings

class Contact(models.Model):
    content = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    introduce = models.TextField(default='hello')

class Theme(models.Model):
    title = models.TextField(null = True,blank = True)
    introduce = models.TextField(null = True,blank = True)
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class SubTheme(models.Model):
    title=  models.TextField()
    theme = models.ForeignKey(Theme,on_delete = models.CASCADE, null = True,blank = True,related_name = 'sub')

class Note(models.Model):
    subTheme = models.ForeignKey(SubTheme,on_delete = models.CASCADE, null = True,blank = True,related_name = 'note')
    theme = models.ForeignKey(Theme,on_delete = models.CASCADE, null = True,blank = True,related_name = 'note')
    title = models.TextField()
    text = models.TextField()
    picture = models.ImageField(upload_to = 'file',null = True,blank = True)
    code = models.TextField(null = True,blank = True)






