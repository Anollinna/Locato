from django.urls import path
from travel.views import (
    LocationListView,
    LocationCreateView,
    LocationUpdateView,
    LocationDeleteView,
    LocationDetailView,
    LocationReviewCreateView,
    ToggleFavoriteView,
    CountryListView,
)

urlpatterns = [
    path(
        "locations/",
        LocationListView.as_view(),
         name="location-list"
    ),
    path(
        "locations/create/",
        LocationCreateView.as_view(),
         name="location-create"
    ),
    path(
        "locations/<int:pk>/update/",
        LocationUpdateView.as_view(),
         name="location-update"
    ),
    path(
        "locations/<int:pk>/delete/",
        LocationDeleteView.as_view(),
         name="location-delete"
    ),
    path(
        "locations/<int:pk>/",
        LocationDetailView.as_view(),
         name="location-detail"
    ),
    path(
        "locations/<int:pk>/add-review/",
         LocationReviewCreateView.as_view(),
         name="location-review"
    ),
    path(
        "locations/<int:pk>/toggle-favorite/",
        ToggleFavoriteView.as_view(),
         name="toggle-favorite"
    ),
    path(
        "countries/",
        CountryListView.as_view(),
         name="countries-list"
    ),
]

app_name = "travel"
