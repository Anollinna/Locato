from django.urls import path

from travel.views import (
    LocationListView,
    LocationCreateView,
    LocationUpdateView,
    LocationDeleteView,
    LocationDetailView,
    LocationReviewCreateView,
    CountryListView,
    TouristListView,
    TouristUpdateView,
    TouristRegisterView,
    TouristDetailView,
    ToggleFavoriteView,
)

urlpatterns = [
    path("locations/", LocationListView.as_view(), name="location-list"),
    path("locations/create/", LocationCreateView.as_view(), name="location-create"),
    path("locations/<int:pk>/update/", LocationUpdateView.as_view(), name="location-update"),
    path("locations/<int:pk>/delete/", LocationDeleteView.as_view(), name="location-delete"),
    path("locations/<int:pk>/", LocationDetailView.as_view(), name="location-detail"),
    path("locations/<int:pk>/add-review/", LocationReviewCreateView.as_view(), name="location-review"),
    path("countries/", CountryListView.as_view(), name="countries-list"),
    path("tourists/", TouristListView.as_view(), name="tourists-list"),
    path("tourists/update/", TouristUpdateView.as_view(), name="tourists-update"),
    path("register/", TouristRegisterView.as_view(), name="register"),
    path("tourists/<int:pk>/", TouristDetailView.as_view(), name="tourists-detail"),
    path("locations/<int:pk>/toggle-favorite/", ToggleFavoriteView.as_view(), name="toggle-favorite"),
]

app_name = "travel"
