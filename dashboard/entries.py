from stakeholders.models import Stakeholder

from .models import Payment


class PaymentAggregation(object):
    def __init__(self, *args, **kwargs):
        self.distributionreport_id = kwargs.get("distributionreport_id")
        self.stakeholder_id = kwargs.get("stakeholder_id")
        self.total_quantity = kwargs.get("total_quantity")
        self.total_earnings = kwargs.get("total_earnings")
        self.total_shares = kwargs.get("total_shares")

    @property
    def stakeholder(self):
        return Stakeholder.objects.get(id=self.stakeholder_id)

    @property
    def paid(self):
        return Payment.objects.filter(
            distributionreport__id=self.distributionreport_id,
            stakeholder__id=self.stakeholder_id,
        ).exists()
