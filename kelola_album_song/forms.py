from django import forms
from .models import Album, Song, Artist, Songwriter, Genre

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['judul', 'label']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['judul', 'duration', 'total_play', 'total_download', 'label', 'artist', 'songwriter', 'genre']
        widgets = {
            'songwriter': forms.CheckboxSelectMultiple(),
            'genre': forms.CheckboxSelectMultiple(),
        }
