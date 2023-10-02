from django import forms

from digitaldistribution.models import Report


class ArtistDetailFilterForm(forms.Form):
    report = forms.ChoiceField(choices=Report.objects.all().values_list("id", "title"))
