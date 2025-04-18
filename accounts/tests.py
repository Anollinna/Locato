from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TouristUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            email="old@example.com"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_update_tourist_info(self):
        url = reverse("accounts:tourists-update")
        data = {
            "username": "updateduser",
            "email": "updated@example.com",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("accounts:tourists-list"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updated@example.com")


class TouristDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_tourist_detail_view(self):
        url = reverse("accounts:tourists-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertTemplateUsed(response, "accounts/tourist_detail.html")
