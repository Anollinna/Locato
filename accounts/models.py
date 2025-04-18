from django.contrib.auth.models import AbstractUser
from django.db import models

from travel.models import Location


class Tourist(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    favorites = models.ManyToManyField(
        Location,
        related_name="favorite_by",
        blank=True
    )

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"{self.username}: ({self.first_name}, {self.last_name})"


class HomepageBanner(models.Model):
    image = models.ImageField(upload_to="homepage_banners/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banner uploaded at {self.uploaded_at}"
