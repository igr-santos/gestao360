import pandas as pd

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from copyright.models import SongHolder
from reports.models import DistributionReport
from reports.split.models import SplitLine
from stakeholders.models import Stakeholder

# from digitaldistribution.models import Report

from .forms import DataframeFilter


# Create your views here.
@login_required
def index(request):
    # Dados de entrada Dafaframe
    # report = Report.objects.first()
    report = DistributionReport.objects.first()

    # Configurações
    dataframe = pd.read_csv(
        report.csv_file.file, delimiter=";", decimal=",", low_memory=False
    )
    offset = 0
    size = 500
    columns = dataframe.columns

    # Processamento dos filtros
    formfilter = DataframeFilter(columns=columns)
    filter_columns = columns

    if request.GET.keys():
        formfilter = DataframeFilter(columns=columns, data=request.GET)
        formfilter.is_valid()

        new_report = formfilter.cleaned_data["report"]
        if new_report:
            report = new_report

            dataframe = pd.read_csv(
                report.csv_file, delimiter=";", decimal=",", low_memory=False
            )

            groupby = formfilter.cleaned_data["groupby"]
            filter_columns = formfilter.cleaned_data["columns"]

            numeric_cols = dataframe.select_dtypes(include=["float64", "int64"]).columns

            if groupby:
                sum_cols = list(filter(lambda x: x in numeric_cols, groupby))
                group_cols = list(filter(lambda x: x not in numeric_cols, groupby))

                dataframe = (
                    dataframe[groupby].groupby(group_cols).sum(sum_cols).reset_index()
                )
            else:
                dataframe = dataframe[filter_columns]
    else:
        report = None
        dataframe = pd.DataFrame()

    return render(
        request,
        "dashboard/index.html",
        {
            "report": report,
            "dataframe": dataframe.loc[offset:size],
            "formfilter": formfilter,
        },
    )


@login_required
def stakeholders(request):
    # stakeholders
    context = {"stakeholders": Stakeholder.objects.all()}

    songholders = []
    stakeholder_id = request.GET.get("pk", None)
    if stakeholder_id:
        stakeholder = Stakeholder.objects.get(pk=stakeholder_id)

        songholders = SongHolder.objects.filter(holder=stakeholder)
        splitlines = SplitLine.objects.filter(owner=stakeholder)

        context.update(
            {
                "stakeholder": stakeholder,
                "songholders": songholders,
                "splitlines": splitlines,
            }
        )

    return render(request, "dashboard/stakeholders.html", context)
