from django.core.management.base import BaseCommand, CommandError

import pandas as pd
from accounts.models import Account, TransactionType
from stakeholders.models import Stakeholder, StakeholderPayment


class Command(BaseCommand):
    # help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("sh_id", type=int)
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        account = Account.objects.get(id=1)
        stakeholder = Stakeholder.objects.get(id=options["sh_id"])
        
        df = pd.read_csv(
            options["filename"],
            delimiter=",",
            decimal=".",
            converters={
                "Data Lançamento": pd.to_datetime,
                "Valor": lambda x: x.replace(".", "").replace(",", "."),
                "Saldo": lambda x: x.replace(".", "").replace(",", "."),
                # "Saldo": pd.to_numeric
            }
        )

        df['Valor'] = df['Valor'].apply(pd.to_numeric)

        
        payments = []
        for x in df.to_dict(orient="records"):
            obj = StakeholderPayment.objects.create(
                recipient=stakeholder,
                origin=account,
                amount=x['Valor'] * -1,
                transaction_date=x['Data Lançamento'],
                transaction_type=TransactionType.credit
            )
            payments.append(obj)

        # payments = StakeholderPayment.objects.bulk_create(payments)
            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)

            # poll.opened = False
            # poll.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully upload transactions "%s"' % len(payments))
        )