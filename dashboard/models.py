from django.db import models

from stakeholders.models import Stakeholder
from reports.models import DistributionReport


# Create your models here.
class ViewSplitSong(models.Model):
    unique_id = models.CharField(primary_key=True)
    title = models.CharField(max_length=200)
    quantity = models.IntegerField()
    split = models.FloatField()
    amount = models.FloatField()
    exchange_amount = models.FloatField(null=True, blank=True)
    income = models.FloatField()
    exchange_income = models.FloatField(null=True, blank=True)

    report_title = models.CharField(max_length=200)
    report_start_date = models.DateField()
    distributionreport_id = models.IntegerField()


    stakeholder_id = models.IntegerField()
    # stakeholder = models.ForeignKey(Stakeholder, on_delete=models.DO_NOTHING)
    # distribution_report = models.ForeignKey(DistributionReport, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "view_split_songs"
    

    @property
    def stakeholder(self):
        return Stakeholder.objects.get(id=self.stakeholder_id)


class Payment(models.Model):
    distributionreport = models.ForeignKey(DistributionReport, on_delete=models.CASCADE)
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    note = models.TextField(null=True, blank=True)