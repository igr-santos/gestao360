from django.contrib import admin
from django.db.models import Count, Sum
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView

# from copyright.models import Song
# from digitaldistribution.models import RoyaltyDivision, Report, ArtistPayment

from .forms import ArtistDetailFilterForm
from .models import Artist


def export_as_pdf(request):
    selected = [int(pk) for pk in request.GET.get("ids", "").split(",")]
    artists = Artist.objects.filter(id__in=selected)

    return render(
        request,
        template_name="stakeholders/export_as_pdf.html",
        context={"artists": artists},
    )


# class ArtistDetailView(PermissionRequiredMixin, DetailView):
#     permission_required = "stakeholders.artist_detail"
#     template_name = "admin/stakeholders/artist/detail.html"
#     model = Artist

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)

#         qs = RoyaltyDivision.objects.filter(recipient=self.get_object())
#         filter_form = ArtistDetailFilterForm()
#         if "report" in self.request.GET:
#             filter_form = ArtistDetailFilterForm(data=self.request.GET)

#             if filter_form.is_valid():
#                 report = filter_form.cleaned_data.get("report")
#                 report = Report.objects.get(pk=report)
#                 payments = ArtistPayment.objects.filter(
#                     recipient=self.get_object(), reference_report=report
#                 ).aggregate(Sum("amount")).get("amount__sum", 0)

#                 ctx["report"] = report
#                 ctx["digitalpayment"] = report.digitalpayment_set.first()
#                 ctx["total_payments"] = payments

#                 qs = qs.filter(sharing__releasesong__reportsongpayment__report=report)
#                 qs = qs.annotate(song_count=Count("sharing__song"))

#         ctx["filter_form"] = filter_form

#         # import ipdb;ipdb.set_trace()
#         ctx["royaltydivision_set"] = qs.order_by("sharing__song__title")

#         return {
#             **ctx,
#             **admin.site.each_context(self.request),
#             "opts": self.model._meta,
#         }
