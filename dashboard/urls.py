"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from .views import stakeholders, generate_pdf, generate_pdf_eur
from .views.financial import payments
from .views.stakeholders import index, reports

urlpatterns = [
    path("", index, name="index"),
    path("auth/", include("django.contrib.auth.urls")),
    path("payments/", payments, name="payments"),
    path("reports/", reports, name="reports"),
    path("stakeholders/", stakeholders, name="stakeholders"),
    path("generate_pdf/<int:stakeholder_id>/<int:report_id>/", generate_pdf, name="generate_pdf"),
    path("generate_pdf_eur/<int:stakeholder_id>/<int:report_id>/", generate_pdf_eur, name="generate_pdf_eur"),
]