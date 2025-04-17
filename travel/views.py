from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from travel.forms import (
    TouristRegistrationForm,
    LocationForm,
    LocationReviewForm,
    TouristUpdateForm,
    HomepageBannerForm
)
from travel.models import Location, LocationReview, Country, Tourist, HomepageBanner


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tourist_count"] = Tourist.objects.count()
        context["location_count"] = Location.objects.count()
        context["city_count"] = Location.objects.values("city").distinct().count()
        context["banner"] = HomepageBanner.objects.order_by("-uploaded_at").first()
        return context


class LocationListView(LoginRequiredMixin, generic.ListView):
    model = Location
    template_name = "travel/location_list.html"
    context_object_name = "locations"
    paginate_by = 6

    def get_queryset(self):
        queryset = Location.objects.select_related("country").all().order_by("-views")

        cities = self.request.GET.getlist("city")
        countries = self.request.GET.getlist("country")
        continents = self.request.GET.getlist("continent")

        if cities:
            queryset = queryset.filter(city__in=cities)
        if countries:
            queryset = queryset.filter(country__id__in=countries)
        if continents:
            queryset = queryset.filter(country__continent__in=continents)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["cities"] = (
            Location.objects
            .exclude(city__isnull=True)
            .exclude(city__exact="")
            .values_list("city", flat=True)
            .distinct()
            .order_by("city")
        )
        context["countries"] = Country.objects.order_by("name")
        context["continents"] = Country.Continent.choices
        context["selected_cities"] = self.request.GET.getlist("city")
        context["selected_countries"] = self.request.GET.getlist("country")
        context["selected_continents"] = self.request.GET.getlist("continent")
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop("page")
        context["query_params"] = query_params.urlencode()

        return context


class LocationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Location
    form_class = LocationForm
    template_name = "travel/location_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.tourists.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse_lazy("travel:location-list")



class LocationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Location
    form_class = LocationForm
    template_name = "travel/location_form.html"
    success_url = reverse_lazy("travel:location-list")


class LocationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Location
    template_name = "travel/location_confirm_delete.html"
    success_url = reverse_lazy("travel:location-list")


class LocationDetailView(FormMixin, generic.DetailView):
    model = Location
    template_name = "travel/location_detail.html"
    context_object_name = "location"
    form_class = LocationReviewForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=["views"])
        return obj

    def get_success_url(self):
        return reverse("travel:location-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["reviews"] = LocationReview.objects.filter(location=self.object).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            review = form.save(commit=False)
            review.tourist = self.request.user
            review.location = self.object
            review.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)


class LocationReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = LocationReview
    form_class = LocationReviewForm
    template_name = "travel/location_review_form.html"

    def form_valid(self, form):
        form.instance.tourist = self.request.user
        form.instance.location = Location.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("travel:location-detail", kwargs={"pk": self.kwargs["pk"]})


class CountryListView(LoginRequiredMixin, generic.ListView):
    model = Country
    template_name = "travel/country_list.html"
    context_object_name = "countries"


class TouristListView(LoginRequiredMixin, generic.ListView):
    model = Tourist
    template_name = "travel/tourist_list.html"
    context_object_name = "tourists"


class TouristRegisterView(generic.CreateView):
    model = Tourist
    form_class = TouristRegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class TouristUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tourist
    form_class = TouristUpdateForm
    template_name = "travel/tourist_form.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("travel:tourists-list")


class TouristDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tourist
    template_name = "travel/tourist_detail.html"
    context_object_name = "tourist"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorite_locations"] = self.object.favorites.all()
        return context


class ToggleFavoriteView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        if location in request.user.favorites.all():
            request.user.favorites.remove(location)
        else:
            request.user.favorites.add(location)
        return redirect(request.META.get("HTTP_REFERER", "travel:location-list"))


class HomepageBannerUploadView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = HomepageBanner
    form_class = HomepageBannerForm
    template_name = "travel/banner_upload.html"
    success_url = "/"

    def test_func(self):
        return self.request.user.is_staff
