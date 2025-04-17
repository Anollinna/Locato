from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django_countries.fields import CountryField


class Tourist(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    favorites = models.ManyToManyField("Location", related_name="favorite_by", blank=True)

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"{self.username}: ({self.first_name}, {self.last_name})"


class Country(models.Model):
    class Continent(models.TextChoices):
        AFRICA = "AF", "Africa"
        EUROPE = "EU", "Europe"
        ASIA = "AS", "Asia"
        NORTH_AMERICA = "NA", "North America"
        SOUTH_AMERICA = "SA", "South America"
        AUSTRALIA = "AU", "Australia"
        ANTARCTICA = "AN", "Antarctica"

    name = CountryField()
    continent = models.CharField(
        max_length=2,
        choices=Continent.choices,
        default=Continent.EUROPE,
    )

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return f"{self.name.name} ({self.get_continent_display()})"


class Location(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="locations")
    tourists = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="locations", blank=True)

    class Meta:
        ordering = ("name", "city", )

    def average_rating(self):
        return self.reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    def __str__(self):
        return f"{self.name} ({self.city})"


class LocationReview(models.Model):
    tourist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tourist", "location"], name="unique_location_review")
        ]

    def __str__(self):
        return f"{self.tourist.username}`s review of {self.location}"
