from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('food/add/', views.add_food, name="add new food"),
    path('menu/add/food/', views.add_to_menu, name='add food to menu'),
]
