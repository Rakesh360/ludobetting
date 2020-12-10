"""ludomission URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from ludoapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('' , include('ludoapp.urls')),
    path('admin/', admin.site.urls),
    path('accounts/' , include('accounts.urls')),
    
    path("",views.playludo,name="index"),
   
    path("help/",views.contactpage,name="help"),
    path("buycoins/",views.buycoins,name="buycoins"),
    path("sellcoins/",views.sellcoins,name="sellcoins"),
    path("history/",views.history,name="history"),
       
    path("terms/",views.terms,name="terms"),
    path("playludo/",views.playludo,name="playludo"),
    path("playsnackladder/",views.playsnackladder,name="playsnackladder"),
   
   
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

