from django.urls import path

from .views import export_songs_contact

urlpatterns = [
    path("export-songs-contact/", export_songs_contact, name="export-songs-contact"),
]
