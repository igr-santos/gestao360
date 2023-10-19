import pandas as pd

from django.db import connection
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from reportlab.pdfgen import canvas

from copyright.models import SongHolder
from reports.models import DistributionReport
from reports.split.models import SplitLine
from stakeholders.models import Stakeholder

# from digitaldistribution.models import Report

from .pdfutils import draw
from .forms import DataframeFilter


@login_required
def index(request):
    return render(request, "dashboard/index.html")


@login_required
def reports(request):
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
        "dashboard/reports.html",
        {
            "report": report,
            "dataframe": dataframe.loc[offset:size],
            "formfilter": formfilter,
        },
    )


@login_required
def stakeholders(request):
    # stakeholders
    context = {"stakeholders": Stakeholder.objects.all().order_by('full_name')}

    songholders = []
    stakeholder_id = request.GET.get("pk", None)
    if stakeholder_id:
        stakeholder = Stakeholder.objects.get(pk=stakeholder_id)

        songholders = SongHolder.objects.filter(holder=stakeholder)
        splitlines = SplitLine.objects.filter(owner=stakeholder).order_by('split__song__title')

        context.update(
            {
                "stakeholder": stakeholder,
                "songholders": songholders,
                "splitlines": splitlines,
            }
        )

    return render(request, "dashboard/stakeholders.html", context)



@login_required
def generate_pdf(request, stakeholder_id, report_id):
    report = DistributionReport.objects.get(pk=report_id)
    stakeholder = Stakeholder.objects.get(pk=stakeholder_id)

    rows = []
    query = f"""
    SELECT
        UPPER(title) as title,
        SUM(exchange_amount) as exchange_amount,
        split,
        SUM(exchange_income) as exchange_income
    FROM public.view_split_songs
    WHERE distributionreport_id = {report.id}
    AND stakeholder_id = {stakeholder.id}
    GROUP BY title, split
    ORDER BY title
"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        # for row in cursor.fetchall():
        #     album, title, amount, split, income = row
            # rows.append(dict(album=album, title=title, amount=amount, split=split, income=income))
    
    amount = sum(map(lambda x: x[-1], rows))
    # rows.insert(0, ["Título", "Rendimento (R$)", "Participação (%)", "Lucro liquido (R$)"])
    # rows.append(["", "", "TOTAL", amount])

    return HttpResponse(draw(
        stakeholder_name=stakeholder.full_name,
        title=f"Relatório: {report.title}",
        header=["Título", "Rendimento (R$)", "Participação (%)", "Lucro liquido (R$)"],
        footer=["", "", "TOTAL", amount],
        rows=rows
    ), content_type='application/pdf')



# def generate_pdf_file(rows):
#     from io import BytesIO
 
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)
 
#     # Create a PDF document
#     books = rows
#     p.drawString(100, 100, "Resumo de ganhos")
 
#     # y = 700
#     # for book in books:
#     #     print(book)
#     #     p.drawString(100, y, f"Album: {book['album']}")
#     #     p.drawString(100, y, f"Title: {book['title']}")
#     #     p.drawString(100, y - 20, f"Rendimento: {book['amount']}")
#     #     p.drawString(100, y - 40, f"Participação: {book['split']}")
#     #     p.drawString(100, y - 60, f"Ganho: {book['income']}")
#     #     y -= 60
 
#     p.showPage()
#     p.save()
 
#     buffer.seek(0)
#     return buffer