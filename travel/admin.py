from django.contrib import admin
from travel.models import (
    Country,
    Location,
    LocationReview
)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "created_at", "updated_at",)
    list_filter = ("country", "city", "created_at", "updated_at",)
    search_fields = ("name",)


@admin.register(LocationReview)
class LocationReviewAdmin(admin.ModelAdmin):
    list_display = ("location", "rating", "comment",)
    list_filter = ("rating",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "continent",)
    list_filter = ("continent",)
