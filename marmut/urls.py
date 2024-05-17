"""marmut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kelola_playlist/', include('kelola_playlist.urls')),
    path('kelola_album_song/', include('kelola_album_song.urls', namespace='kelola_album_song')),
    path('play_song/', include('play_song.urls')),
    path('login/', include('login.urls')),
    path('', include('main.urls')),
    path('downloaded_song/', include('downloaded_song.urls')),
    path('play_playlist/', include('play_playlist.urls')),
    path('register/', include('register.urls')),
    path('cek_royalti/', include('cek_royalti.urls')),
]
