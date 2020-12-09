from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from django.core.signing import Signer
# Create your models here.

class User(models.Model):
    id          =  models.AutoField(primary_key=True)
    username    =  models.CharField(max_length=255, default=None, blank=True)   # make sure that no other user is available with the same username
    email       =  models.EmailField(default=None, blank=True)
    password    =  models.CharField(max_length=100, default="")
    role        =  models.IntegerField(default=0)  # 1: restaurant | 2: normal
    isLogedIn   =  models.BooleanField(default=False)
    token       =  models.CharField(max_length=32, blank=True)

    def save(self, *args, **kwargs):
        if self.role == 1:
            signer = Signer()
            self.token = signer.sign(str(self.username) + str(self.password))
        super(User, self).save(*args, **kwargs)



    def __str__(self):
        if self.username != None:
            return self.username
        else:
            return self.token
