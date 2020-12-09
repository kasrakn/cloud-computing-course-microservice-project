from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurant/', include('panel.restaurant.urls')),
    path('menu/', include('panel.menu.urls')),
    path('enter/', views.enter, name='guest enter'),
    path('exit/', views.exit, name='guest exit'),
]
