from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('auth/users/', views.user, name='signup'),
    path('auth/users/<int:pk>', views.user_detail, name='show the user info'),
    path('auth/users/login', views.login, name='login'),
    path('auth/check/', views.authentication_checker, name='check the authentication')
]