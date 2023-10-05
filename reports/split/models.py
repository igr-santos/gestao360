from django.db import models

from copyright.models import Song
from reports.models import DistributionReport
from stakeholders.models import Stakeholder


class Split(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return self.song.title

class KindSplitLine(models.TextChoices):
    artist = "artist", "Artista principal"
    feature = "feature", "Participação Especial"
    manager = "manager", "Produtor Fonográfico"


class SplitLine(models.Model):
    split = models.ForeignKey(Split, on_delete=models.CASCADE)
    owner = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    kind = models.CharField(max_length=30, choices=KindSplitLine.choices)
    value = models.DecimalField(max_digits=6, decimal_places=3)


class SplitSong(models.Model):
    split = models.ForeignKey(Split, on_delete=models.SET_NULL, null=True, blank=True)
    album = models.CharField(max_length=100)
    title = models.CharField(max_length=100)


class SplitReportPayment(models.Model):
    report = models.ForeignKey(DistributionReport, on_delete=models.CASCADE)
    split_song = models.ForeignKey(SplitSong, on_delete=models.CASCADE)
    amount = models.FloatField()

    @property
    def title(self):
        return self.split_song.title
