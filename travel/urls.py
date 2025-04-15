from django.urls import path

urlpatterns = [
    path("", LocationListView.as_view(), name="location-list"),

]

app_name = "traveling"