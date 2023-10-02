from django.db import models
from stakeholders.models import Stakeholder


# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=80)
    ecad = models.CharField(max_length=20, null=True, blank=True)
    iswc = models.CharField(max_length=20, null=True, blank=True)
    is_editor = models.BooleanField(default=True)

    def __str__(self):
        royalties_share_sum = sum(
            self.songholder_set.all().values_list("royalties_share", flat=True)
        )

        return f"{self.title} ({royalties_share_sum})"


class CategorySongHolder(models.TextChoices):
    author = "author", "Compsitor/Autor"
    published = "published", "Editor"


class SongHolder(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    holder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=CategorySongHolder.choices)
    royalties_share = models.DecimalField(decimal_places=3, max_digits=5)

    def __str__(self):
        return f"{self.holder.full_name} ({self.royalties_share})"
