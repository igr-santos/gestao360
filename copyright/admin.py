from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Song, SongHolder


@admin.action(description="Open songs list")
def export_selected_objects(modeladmin, request, queryset):
    selected = queryset.values_list("pk", flat=True)

    return HttpResponseRedirect(
        reverse("export-songs-contact") + f"?ids={','.join(str(pk) for pk in selected)}"
    )


class SongHolderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["holder"]


class SongHolderInline(admin.TabularInline):
    model = SongHolder
    autocomplete_fields = ["holder"]
    extra = 0


class SongAdmin(admin.ModelAdmin):
    inlines = [SongHolderInline]
    ordering = ["title"]
    actions = [export_selected_objects]
    search_fields = ["title", ]


# Register your models here.
admin.site.register(Song, SongAdmin)
admin.site.register(SongHolder, SongHolderAdmin)
