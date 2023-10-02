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


class DistributionReport(ReportAbstractBase):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    @property
    def amount(self):
        return round(sum(map(lambda x: x['lucro_liquido'], self.json_data)), 2)