from django.db import models


# Create your models here.
class Stakeholder(models.Model):
    full_name = models.CharField(max_length=180)
    artist_name = models.CharField(max_length=100)
    related_artist = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


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