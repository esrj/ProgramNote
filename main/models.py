from django.db import models
from django.contrib.auth.models import AbstractUser


class Contact(models.Model):
    content = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class Theme(models.Model):
    note_title = models.TextField(null = True,blank = True)
    introduce =models.TextField(null = True,blank = True)

class Sub_Theme(models.Model):
    sub_title=  models.TextField()
    main_title = models.ForeignKey(Theme,on_delete = models.CASCADE, null = True,blank = True,related_name = 'sub')


class Note(models.Model):
    sub_theme = models.ForeignKey(Sub_Theme,on_delete = models.CASCADE, null = True,blank = True,related_name = 'sub_name')
    theme = models.ForeignKey(Theme,on_delete = models.CASCADE, null = True,blank = True,related_name = 'note')
    title = models.TextField()
    text = models.TextField()
    picture = models.ImageField(upload_to = 'file',null = True,blank = True)
    code = models.TextField(null = True,blank = True)



class User(AbstractUser):
    introduce = models.TextField(default='hello')




