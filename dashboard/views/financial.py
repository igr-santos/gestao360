from django.db.models import Count, Sum
from django.shortcuts import render

from dashboard.entries import PaymentAggregation
from dashboard.models import ViewSplitSong
from reports.models import DistributionReport


def payments(request):
    distributionreport = DistributionReport.objects.order_by("-end_date").first()

    qs = ViewSplitSong.objects.filter(distributionreport_id=distributionreport.id)

    payments = sorted(
        list(
            map(
                lambda kwargs: PaymentAggregation(distributionreport_id=distributionreport.id, **kwargs),
                (
                    qs.values("stakeholder_id")
                    .order_by("stakeholder_id")
                    .annotate(
                        total_shares=Count("unique_id"),
                        total_quantity=Sum("quantity"),
                        total_earnings=Sum("exchange_income"),
                    )
                ),
            )
        ),
        key=lambda x: -x.total_earnings,
    )

    context = {"distributionreport": distributionreport, "payments": payments}

    return render(
        request, template_name="dashboard/financial/payments.html", context=context
    )


# def pay(request, stakeholder_id, distributionreport_id):
