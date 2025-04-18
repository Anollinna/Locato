from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import Tourist, HomepageBanner


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
