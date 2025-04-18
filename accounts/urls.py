from django.urls import path
from accounts.views import (
    TouristListView,
    TouristUpdateView,
    TouristRegisterView,
    TouristDetailView,
    HomepageBannerUploadView
)

urlpatterns = [
    path(
        "tourists/",
        TouristListView.as_view(),
         name="tourists-list"
    ),
    path(
        "tourists/update/",
        TouristUpdateView.as_view(),
         name="tourists-update"
    ),
    path(
        "register/",
        TouristRegisterView.as_view(),
         name="register"
    ),
    path(
        "tourists/<int:pk>/",
         TouristDetailView.as_view(),
         name="tourists-detail"
    ),

    path(
        "banners-upload/",
        HomepageBannerUploadView.as_view(),
         name="banner-upload"
    ),
]

app_name = "accounts"
