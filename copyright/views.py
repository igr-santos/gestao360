from django.shortcuts import render

from .models import Song


# Create your views here.
def export_songs_contact(request):
    selected = [int(pk) for pk in request.GET.get("ids", "").split(",")]
    songs = Song.objects.filter(id__in=selected)

    return render(
        request,
        template_name="copyright/export_songs_contact.html",
        context={"songs": songs},
    )
