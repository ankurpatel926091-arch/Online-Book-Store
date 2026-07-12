from django.db import models

# Create your models here.
class Enquiry(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    contactno=models.CharField(15)
    subject=models.CharField(max_length=200)
    message=models.TextField
    enqdate=models.DateTimeField(auto_now=True)

class LoginInfo(models.Model):
     usertype=models.CharField(max_length=15, default='user')
     username=models.CharField(max_length=200, unique=True)
     password=models.CharField(max_length=256)
     def __str__(self):
          return f"{self.username}->{(self.usertype)}"

class Userinfo(models.Model):
     login=models.OneToOneField(LoginInfo, on_delete=models.CASCADE)
     name=models.CharField(max_length=100)
     email=models.CharField(max_length=100)
     contactno=models.CharField(max_length=15)
     address=models.TextField()
     picture=models.ImageField(upload_to='user_profiles')
    #  def __str__(self):
    #     return f"(self.usernfo)->{(self.usertype)}"
