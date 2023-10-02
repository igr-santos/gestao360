from django_select2 import forms as s2forms


class HolderWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "full_name__icontains",
        "artist_name__icontains"
    ]