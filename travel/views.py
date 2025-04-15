from msilib.schema import ListView

from django.shortcuts import render

from traveling.models import Location


class LocationListView(LoListView):
    model = Location
