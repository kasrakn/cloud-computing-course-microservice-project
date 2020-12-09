from django.urls import path
from . import views

urlpatterns = [

    path('restaurant/', views.get_restaurants, name='get restaurants'),
    path('restaurant/menu/', views.get_menu, name='get restaurants'),
    path('restaurant/close/', views.close_restaurant, name='close restaurant'),
    path('restaurant/open/', views.open_restaurant, name='open restaurant'),
    path('restaurant/status/', views.restaurant_status, name='restaurant status'),
]
