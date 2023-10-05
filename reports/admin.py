import pandas as pd

from typing import Any

from django.contrib import admin
from django.utils.text import slugify

from .models import DistributionReport
from .split.models import SplitReportPayment, SplitSong


class ReportBelieveAdmin(admin.ModelAdmin):
    index_columns = [{"album": "Título do lançamento"}, {"title": "Titulo da faixa"}]
    sum_columns = ["Lucro Líquido"]

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)
        # TODO: Relatório Generico

        if not SplitReportPayment.objects.filter(report=obj).exists():
            df = pd.read_csv(
                obj.csv_file, delimiter=";", decimal=",", date_format="%d/%m/%Y"
            )

            groupby = list(map(lambda x: "".join(x.values()), self.index_columns))
            columns = groupby + self.sum_columns

            df = pd.DataFrame(df[columns].groupby(by=groupby).sum())
            df = df.reset_index()

            for row in df.to_dict(orient="records"):
                params = dict(
                    [
                        ("".join(x.keys()), row["".join(x.values())])
                        for x in self.index_columns
                    ]
                )
                split_song, created = SplitSong.objects.get_or_create(**params)

                SplitReportPayment.objects.get_or_create(
                    report=obj, split_song=split_song, amount=row[self.sum_columns[0]]
                )


class DistributionReportAdmin(ReportBelieveAdmin):
    list_display = ("title", "amount")
    fields = ("title", "csv_file", "income")

    def save_model(
        self, request: Any, obj: DistributionReport, form: Any, change: Any
    ) -> None:
        if not change:
            df = pd.read_csv(
                obj.csv_file, delimiter=";", decimal=",", date_format="%d/%m/%Y"
            )
            df = df.fillna("")
            naming = lambda x: slugify(x).replace("-", "_")

            obj.columns = dict((naming(col), col) for col in df.columns)
            obj.dtypes = dict(
                (naming(col), str(dtype)) for col, dtype in zip(df.columns, df.dtypes)
            )

            df = df.rename(
                columns=dict(
                    (value, key)
                    for (key, value) in zip(obj.columns.keys(), obj.columns.values())
                )
            )
            obj.json_data = df.to_dict(orient="records")

        obj.update_amount()
        super().save_model(request, obj, form, change)


admin.site.register(DistributionReport, DistributionReportAdmin)
