from django import forms
from django.contrib.auth.forms import UserCreationForm
from travel.models import Location, LocationReview, Tourist, HomepageBanner


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "city", "description", "image", "country"]


class LocationReviewForm(forms.ModelForm):
    class Meta:
        model = LocationReview
        fields = ["rating", "comment"]


class TouristRegistrationForm(UserCreationForm):
    class Meta:
        model = Tourist
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "password1",
            "password2"
        ]


class TouristUpdateForm(forms.ModelForm):
    class Meta:
        model = Tourist
        fields = ["username", "first_name", "last_name", "email", "bio"]


class HomepageBannerForm(forms.ModelForm):
    class Meta:
        model = HomepageBanner
        fields = ['image']
