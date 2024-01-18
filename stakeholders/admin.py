from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Stakeholder, Contact, ContactCard, StakeholderPayment
# from .views import ArtistDetailView


@admin.action(description="Open contact list")
def export_selected_objects(modeladmin, request, queryset):
    selected = queryset.values_list("pk", flat=True)

    return HttpResponseRedirect(
        reverse("export-as-pdf")
        + f"?ids={','.join(str(pk) for pk in selected)}"
    )


class ArtistAdmin(admin.ModelAdmin):
    actions = [export_selected_objects]
    search_fields = ["full_name", "artist_name"]
    list_display = ['artist_name', 'full_name', "user"]

    # def get_urls(self):
    #     return [
    #         path(
    #             "<pk>/defailt",
    #             self.admin_site.admin_view(ArtistDetailView.as_view()),
    #             name="songholders_artist_detail"
    #         ),
    #         *super().get_urls(),
    #     ]

    # def detail(self, obj: Artist):
    #     url = reverse("admin:songholders_artist_detail", args=[obj.pk])
    #     return format_html(f'<a href="{url}">📝</a>')


class StakeholderPaymentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["recipient"]
    list_display = ["description", "transaction_date", "recipient", "transaction_type", "amount"]
    list_display_links = ["description", "recipient"]
    ordering = ["-transaction_date"]
    search_fields = ["recipient__full_name", ]

# Register your models here.
admin.site.register(Stakeholder, ArtistAdmin)
admin.site.register(Contact)
admin.site.register(ContactCard)
admin.site.register(StakeholderPayment, StakeholderPaymentAdmin)