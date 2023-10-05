from django.db import models


# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.name}*{self.account_number}"


class TransactionType(models.TextChoices):
    credit = "credit", "Credito"
    debit = "debit", "Debito"


class Transaction(models.Model):
    origin = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_date = models.DateField(null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    description = models.TextField()