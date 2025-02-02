from django.urls import include, path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('newdream', newdream, name='newdream'),
    path('get_dreams', get_dreams, name='get_dreams'),
]