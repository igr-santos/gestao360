from django.contrib import admin

from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["distributionreport", "stakeholder"]
    # search_fields = ["distributionreport", "stakeholder"]
    list_display = ['stakeholder', 'distributionreport', 'note']

admin.site.register(Payment, PaymentAdmin)