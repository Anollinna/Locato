from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from traveling.models import Country, Location, LocationReview,Tourist


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country", "created_at", "updated_at",)
    list_filter = ("country", "city", "created_at", "updated_at",)
    search_fields = ("name",)


@admin.register(LocationReview)
class LocationReviewAdmin(admin.ModelAdmin):
    list_display = ("location", "rating", "comment",)
    list_filter = ("rating",)


@admin.register(Tourist)
class TouristAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("bio",)
    fieldsets = UserAdmin.fieldsets + (("Additional Information", {"fields": ("bio",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional Information", {"fields": ("first_name", "last_name", "bio",)}),)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "continent",)
    list_filter = ("continent",)
