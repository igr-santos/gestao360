import json

from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from reports.models import DistributionReport, DistributionReportPaymentStatus

# from reports.split.models import SplitLine
from dashboard.dbutils import view_reports
from dashboard.models import ViewSplitSong
from dashboard.forms import StakeholderReportFilter


@login_required
def index(request):
    stakeholder = request.user.stakeholder_set.first()
    report = DistributionReport.objects.last()

    qs = ViewSplitSong.objects.filter(
        stakeholder_id=stakeholder.id, distributionreport_id=report.id
    )

    split_songs = qs.order_by("-income", "-title")
    reports = view_reports(stakeholder, "2020-01-01")

    labels = list(map(lambda x: x["title"], reports))
    values = list(map(lambda x: float(x["exchange_income"]), reports))

    ctx = {
        "report": report,
        "split_songs": split_songs[:5],
        "chart": {"labels": json.dumps(labels), "values": json.dumps(values)},
    }

    if report.payment_status == DistributionReportPaymentStatus.opened:
        ctx.update(
            {
                "next_payment": {
                    "currency": "EUR",
                    "value": round(sum(list(map(lambda x: x.income, split_songs))), 2),
                }
            }
        )
    elif report.payment_status == DistributionReportPaymentStatus.processing:
        ctx.update(
            {
                "next_payment": {
                    "currency": "PREV",
                    "value": round(
                        sum(list(map(lambda x: x.exchange_income, split_songs))), 2
                    ),
                }
            }
        )
    elif report.payment_status == DistributionReportPaymentStatus.done:
        ctx.update(
            {
                "next_payment": {
                    "currency": "BRL",
                    "value": round(
                        sum(list(map(lambda x: x.exchange_income, split_songs))), 2
                    ),
                }
            }
        )

    return render(request, "dashboard/stakeholders/index.html", ctx)


@login_required
def reports(request):
    stakeholder = request.user.stakeholder_set.first()

    reports = (
        ViewSplitSong.objects.filter(stakeholder_id=stakeholder.id)
        .values("distributionreport_id", "report_title", "report_start_date")
        .annotate(count=Count("report_title"))
        .order_by("-report_start_date")
    )

    form = StakeholderReportFilter(
        data=request.GET,
        choices=list(
            map(lambda x: (x["distributionreport_id"], x["report_title"]), reports)
        ),
    )

    ctx = {"filter": form, "reports": reports, "split_songs": []}

    if form.is_valid() and form.cleaned_data["report"]:
        split_songs = ViewSplitSong.objects.filter(
            stakeholder_id=stakeholder.id,
            distributionreport_id=form.cleaned_data["report"],
        ).order_by("title")
        ctx.update({"split_songs": split_songs})

    return render(request, "dashboard/stakeholders/reports.html", ctx)
