from django import forms
from travel.models import Location, LocationReview


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "city", "description", "image", "country"]


class LocationReviewForm(forms.ModelForm):
    class Meta:
        model = LocationReview
        fields = ["rating", "comment"]
