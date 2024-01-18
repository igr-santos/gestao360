from django.db import models

# from django.contrib.postgres.fields import ArrayField


# Create your models here.
class ReportAbstractBase(models.Model):
    csv_file = models.FileField(upload_to="reports/datafiles/")
    # Parse CSV to matrix json for after use
    json_data = models.JSONField(null=True, blank=True)
    columns = models.JSONField(null=True, blank=True)
    dtypes = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True


class DistributionReportPaymentStatus(models.TextChoices):
    done = "done", "Concluído"
    processing = "processing", "Processando"
    opened = "opened", "Aberto"


class DistributionReport(ReportAbstractBase):
    title = models.CharField(max_length=100)
    amount = models.FloatField(null=True, blank=True)
    income = models.FloatField(null=True, blank=True)
    payment_status = models.CharField(
        choices=DistributionReportPaymentStatus.choices,
        default=DistributionReportPaymentStatus.opened,
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    def update_amount(self):
        """Update amount field with sum lucro_liquido rows"""
        if not self.amount:
            self.amount = sum(map(lambda x: x["lucro_liquido"], self.json_data))
