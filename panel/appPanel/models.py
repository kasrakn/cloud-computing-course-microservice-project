from django.db import models
# Create your models here.

class Food(models.Model):
    foodID      =   models.AutoField(primary_key=True)
    name        =   models.CharField(max_length=255)
    price       =   models.FloatField(default=0)
    availablity =   models.IntegerField(default=0)

    def __str__(self):
        return self.name
  
class Menu(models.Model):
    id      =   models.AutoField(primary_key=True)
    name    =   models.CharField(max_length=100)
    foods   =   models.ManyToManyField(Food, default=None)
    username  = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Order(models.Model):
    foods       = models.ManyToManyField(Food)
    total_price = models.FloatField(default=None)
    status  = models.BooleanField(default=True)

    @classmethod
    def calcute_price(cls):
        pass


class Restaurant(models.Model):
    menus      =   models.ManyToManyField(Food, blank=True, default=None)
    orders     =   models.ManyToManyField(Order, blank=True)
    is_open    =   models.BooleanField(default=True)
    username   =   models.CharField(max_length=32, blank=True)