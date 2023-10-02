from django.contrib import admin
from django.db.models import Sum

from .models import SplitReportPayment, SplitSong, Split, SplitLine


class SplitLineInline(admin.TabularInline):
    model = SplitLine
    extra = 1
    autocomplete_fields = ["owner"]


class SplitAdmin(admin.ModelAdmin):
    autocomplete_fields = ["song"]
    inlines = [SplitLineInline]
    search_fields = ["song__title"]


class SplitReportPaymentAdmin(admin.ModelAdmin):
    list_display = ("title", "amount")
    list_filter = ["report"]
    change_list_template = "admin/reports/split/change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        # Extract the final queryset from the ChangeList object
        change_list = response.context_data["cl"]
        queryset = change_list.queryset

        # Add context
        qs = queryset.aggregate(sum=Sum("amount"))
        response.context_data["rows_amount_sum"] = round(qs["sum"] or 0, 2)

        return response


class SplitSongAdmin(admin.ModelAdmin):
    autocomplete_fields = ["split"]
    search_fields = ["album", "title"]
    list_display = ["title", "album", "has_split"]
    # filter_horizontal = ["has_song"]

    @admin.display(boolean=True, description="Has song?", ordering="-split")
    def has_split(self, obj):
        return obj.split is not None


admin.site.register(SplitReportPayment, SplitReportPaymentAdmin)
admin.site.register(SplitSong, SplitSongAdmin)
admin.site.register(Split, SplitAdmin)