from django.contrib.auth import login
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import (
    TouristRegistrationForm,
    TouristUpdateForm,
    HomepageBannerForm
)
from accounts.models import Tourist, HomepageBanner


class TouristListView(LoginRequiredMixin, generic.ListView):
    model = Tourist
    template_name = "accounts/tourist_list.html"
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
    template_name = "accounts/tourist_form.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("travel:tourists-list")


class TouristDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tourist
    template_name = "accounts/tourist_detail.html"
    context_object_name = "tourist"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorite_locations"] = self.object.favorites.all()
        return context


class HomepageBannerUploadView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.CreateView
):
    model = HomepageBanner
    form_class = HomepageBannerForm
    template_name = "accounts/banner_upload.html"
    success_url = "/"

    def test_func(self):
        return self.request.user.is_staff
