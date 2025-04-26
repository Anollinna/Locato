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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].widget.attrs.update({
            "class": "form-control",
            "type": "number",
            "min": "1",
            "max": "5",
            "step": "1"
        })
        self.fields["comment"].widget.attrs.update({
            "class": "form-control",
            "rows": "4"
        })

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5")
        return rating
