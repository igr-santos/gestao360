from django.db import connection, models
from django.db.models import Sum
# from django.db.models.expressions import RawSQL

from accounts.models import Transaction
from reports.models import DistributionReport


# Create your models here.
class Stakeholder(models.Model):
    full_name = models.CharField(max_length=180)
    artist_name = models.CharField(max_length=100)
    related_artist = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    @property
    def earnings_brl(self):
        amount = 0

        with connection.cursor() as cursor:
            query = f"""
                select
                    sum(agg.amount * agg.ratio) as amount
                from (
                    select
                        sum((sp.amount * (sl.value / 100))) as amount,
                        (dr.income / dr.amount) as ratio,
                        dr.id as report_id
                    from split_splitreportpayment sp
                    inner join split_splitsong ss on ss.id = sp.split_song_id
                    inner join split_splitline sl on sl.split_id = ss.split_id
                    inner join stakeholders_stakeholder sh on sh.id = sl.owner_id
                    inner join reports_distributionreport dr on dr.id = sp.report_id
                    where sh.id = {self.id}
                    group by dr.id, dr.income, dr.amount
                ) as agg
            """
            cursor.execute(query)
            row = cursor.fetchone()
            amount = row[0]
        
        return round(amount or 0, 2)

    @property
    def get_sum_reports(self):
        items = []
        amount = 0

        with connection.cursor() as cursor:
            query = f"""
                select
                    sum((sp.amount * (sl.value / 100))) as amount,
                    (dr.income / dr.amount) as ratio,
                    dr.id as report_id
                from split_splitreportpayment sp
                inner join split_splitsong ss on ss.id = sp.split_song_id
                inner join split_splitline sl on sl.split_id = ss.split_id
                inner join stakeholders_stakeholder sh on sh.id = sl.owner_id
                inner join reports_distributionreport dr on dr.id = sp.report_id
                where sh.id = {self.id}
                group by dr.id, dr.income, dr.amount
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                amount, ratio, report_id = row
                items.append({
                    "report": DistributionReport.objects.get(pk=report_id),
                    "amount_brl": round(amount * ratio, 2),
                    "amount": round(amount or 0, 2)
                })

        
        return items

    @property
    def income(self):
        agg = StakeholderPayment.objects.filter(recipient=self).aggregate(amount=Sum("amount"))
        return agg.get("amount", 0)

    @property
    def debit(self):
        return round((self.earnings_brl or 0) - (self.income or 0), 2)


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