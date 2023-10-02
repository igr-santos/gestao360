from django.urls import path

from .views import export_as_pdf

urlpatterns = [
    path("export-as-pdf/", export_as_pdf, name="export-as-pdf"),
]
