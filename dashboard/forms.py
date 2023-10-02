from django import forms
from django.utils.functional import lazy

from reports.models import DistributionReport


class DataframeFilter(forms.Form):
    report = forms.ModelChoiceField(queryset=DistributionReport.objects, required=False, label="Relatório")

    columns = forms.MultipleChoiceField(
        label="Colunas", required=False, widget=forms.CheckboxSelectMultiple()
    )

    groupby = forms.MultipleChoiceField(
        label="Agrupar", required=False, widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, columns: [str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_fields["columns"].choices = list(map(lambda x: (x, x), columns))

        self.base_fields["groupby"].choices = list(map(lambda x: (x, x), columns))
