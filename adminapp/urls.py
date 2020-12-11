from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
       path('disputed/' , disputed , name="disputed"),
       path('disputed/show/<id>' , show_disputed , name="show_disputed")
]