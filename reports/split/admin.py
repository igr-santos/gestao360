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