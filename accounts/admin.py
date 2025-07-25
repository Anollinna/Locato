from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Tourist, HomepageBanner


@admin.register(Tourist)
class TouristAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("bio",)
    fieldsets = (
            UserAdmin.fieldsets +
            (("Additional Information", {"fields": ("bio",)}),))
    add_fieldsets = (
            UserAdmin.add_fieldsets +
            (("Additional Information",
              {"fields": ("first_name", "last_name", "bio",)}),))


@admin.register(HomepageBanner)
class HomepageBannerAdmin(admin.ModelAdmin):
    list_display = ("id", "uploaded_at")
    ordering = ("-uploaded_at",)
