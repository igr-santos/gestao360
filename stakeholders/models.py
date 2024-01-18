from django.db import connection, models
from django.db.models import Sum
from django.contrib.auth.models import User
# from django.db.models.expressions import RawSQL

from accounts.models import Transaction
from reports.models import DistributionReport


# Create your models here.
class Stakeholder(models.Model):
    full_name = models.CharField(max_length=180)
    artist_name = models.CharField(max_length=100)
    related_artist = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_detail = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.full_name

    @property
    def earnings_brl(self):
        amount = 0

        with connection.cursor() as cursor:
            query = f"""
                SELECT
                    SUM(ss.exchange_income) as exchange_income
                FROM public.view_split_songs as ss
                INNER JOIN public.reports_distributionreport dr ON dr.id = ss.distributionreport_id 
                WHERE ss.stakeholder_id = {self.id}
                AND dr.payment_status = 'done'
            """
            cursor.execute(query)
            row = cursor.fetchone()
            amount = row[0]
        
        return amount or 0

    @property
    def get_sum_reports(self):
        items = []
        amount = 0

        with connection.cursor() as cursor:
            query = f"""
                SELECT
                    ss.distributionreport_id,
                    ROUND(SUM(ss.amount)::numeric, 2) as amount,
                    SUM(ss.exchange_amount) as exchange_amount,
                    ROUND(SUM(ss.income)::numeric, 2) as income,
                    SUM(ss.exchange_income) as exchange_income
                FROM public.view_split_songs as ss
                INNER JOIN reports_distributionreport dr ON dr.id = ss.distributionreport_id
                WHERE ss.stakeholder_id = {self.id}
                GROUP BY ss.distributionreport_id, dr.start_date
                ORDER BY dr.start_date desc
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                report_id, amount, exchange_amount, income, exchange_income = row
                items.append({
                    "report": DistributionReport.objects.get(pk=report_id),
                    "amount": amount,
                    "exchange_amount": exchange_amount,
                    "income": income,
                    "exchange_income": exchange_income,
                })

        return items

    @property
    def income(self):
        agg = StakeholderPayment.objects.filter(recipient=self).aggregate(amount=Sum("amount"))
        return round(agg.get("amount") or 0, 2)

    @property
    def debit(self):
        return round(float(self.earnings_brl or 0) - float(self.income or 0), 2)


class ContactChoices(models.TextChoices):
    phone = "phone", "Telefone"
    email = "email", "Email"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=20, choices=ContactChoices.choices)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.kind})"


class ContactCard(models.Model):
    artist = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(Contact)

    def __str__(self):
        return f"{self.artist.full_name} ({self.contacts.count()})"


class StakeholderPayment(Transaction):
    recipient = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipient.full_name