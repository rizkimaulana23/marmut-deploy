from django.shortcuts import render

# Create your views here.
def show_downloaded_song(request):
    return render(request, 'downloaded_song/show_downloaded_song.html')