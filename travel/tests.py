from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from travel.models import Country, Location, Tourist, LocationReview


class LocationListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Tourist.objects.create_user(
            username="testuser",
            password="password123"
        )
        cls.country1 = Country.objects.create(name="UA", continent="EU")
        cls.country2 = Country.objects.create(name="CA", continent="NA")

        cls.location1 = Location.objects.create(
            name="Kyiv Castle",
            city="Kyiv",
            description="Historic castle in Kyiv.",
            country=cls.country1
        )
        cls.location2 = Location.objects.create(
            name="Lviv Opera",
            city="Lviv",
            description="Beautiful opera house.",
            country=cls.country1
        )
        cls.location3 = Location.objects.create(
            name="CN Tower",
            city="Toronto",
            description="Tall tower in Canada.",
            country=cls.country2
        )

    def setUp(self):
        self.client.login(username="testuser", password="password123")

    def test_location_list_view_status_code(self):
        response = self.client.get(reverse("travel:location-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/location_list.html")

    def test_locations_displayed(self):
        response = self.client.get(reverse("travel:location-list"))
        self.assertContains(response, "Kyiv Castle")
        self.assertContains(response, "Lviv Opera")
        self.assertContains(response, "CN Tower")

    def test_filter_by_city(self):
        response = self.client.get(
            reverse("travel:location-list") + "?city=Kyiv")
        self.assertContains(response, "Kyiv Castle")
        self.assertNotContains(response, "Lviv Opera")
        self.assertNotContains(response, "CN Tower")

    def test_filter_by_country(self):
        response = self.client.get(reverse(
            "travel:location-list") + f"?country={self.country2.pk}")
        self.assertContains(response, "CN Tower")
        self.assertNotContains(response, "Kyiv Castle")

    def test_filter_by_continent(self):
        response = self.client.get(reverse(
            "travel:location-list") + "?continent=EU")
        self.assertContains(response, "Kyiv Castle")
        self.assertContains(response, "Lviv Opera")
        self.assertNotContains(response, "CN Tower")


class LocationDetailViewTests(TestCase):

    def setUp(self):
        self.user = Tourist.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.country = Country.objects.create(
            name="Country",
            continent=Country.Continent.EUROPE
        )
        self.location = Location.objects.create(
            name="Test Location",
            city="Test City",
            description="Test description",
            country=self.country
        )
        self.client.login(username="testuser", password="testpassword")

    def test_add_review(self):
        data = {"rating": 4, "comment": "Nice place!"}
        response = self.client.post(reverse("travel:location-detail",
                                            args=[self.location.pk]), data)
        self.assertRedirects(response, reverse("travel:location-detail",
                                               args=[self.location.pk]))
        self.assertTrue(
            LocationReview.objects.filter(comment="Nice place!").exists())

    def test_add_multiple_reviews(self):
        data1 = {"rating": 4, "comment": "Nice place!"}
        response1 = self.client.post(reverse("travel:location-detail",
                                             args=[self.location.pk]), data1)
        self.assertRedirects(response1,
                             reverse("travel:location-detail",
                                     args=[self.location.pk]))
        self.assertEqual(
            LocationReview.objects.filter(location=self.location,
                                          tourist=self.user).count(), 1)
        data2 = {"rating": 5, "comment": "Amazing experience!"}
        if not LocationReview.objects.filter(
                location=self.location,
                tourist=self.user).exists():
            response2 = self.client.post(
                reverse("travel:location-detail",
                        args=[self.location.pk]), data2)
            self.assertRedirects(
                response2,
                reverse("travel:location-detail",
                        args=[self.location.pk])
            )
        else:
            response2 = self.client.get(
                reverse("travel:location-detail",
                        args=[self.location.pk])
            )
        self.assertEqual(
            LocationReview.objects.filter(
                location=self.location,
                tourist=self.user).count(),
            1
        )


class ToggleFavoriteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Tourist.objects.create_user(
            username="testuser",
            password="password123"
        )
        cls.country = Country.objects.create(name="UA", continent="EU")
        cls.location = Location.objects.create(
            name="Kyiv Castle",
            city="Kyiv",
            description="Historic castle in Kyiv.",
            country=cls.country
        )

    def setUp(self):
        self.client.login(username="testuser", password="password123")

    def test_add_to_favorites(self):
        response = self.client.post(
            reverse("travel:toggle-favorite",
                    args=[self.location.pk])
        )
        self.assertRedirects(response, reverse("travel:location-list"))
        self.user.refresh_from_db()
        self.assertIn(self.location, self.user.favorites.all())

    def test_remove_from_favorites(self):
        self.user.favorites.add(self.location)
        response = self.client.post(
            reverse("travel:toggle-favorite",
                    args=[self.location.pk])
        )
        self.assertRedirects(response, reverse("travel:location-list"))
        self.user.refresh_from_db()
        self.assertNotIn(self.location, self.user.favorites.all())


class LocationCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Tourist.objects.create_user(
            username="testuser",
            password="password123"
        )
        cls.country = Country.objects.create(name="UA", continent="EU")

    def setUp(self):
        self.client.login(username="testuser", password="password123")

    def test_create_location_view_status_code(self):
        response = self.client.get(reverse("travel:location-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/location_form.html")

    def test_create_location_success(self):
        data = {
            "name": "New Location",
            "city": "Lviv",
            "description": "New place in Lviv",
            "country": self.country.pk
        }
        response = self.client.post(reverse("travel:location-create"), data)
        self.assertRedirects(response, reverse("travel:location-list"))
        self.assertTrue(Location.objects.filter(name="New Location").exists())

    def test_create_location_invalid_data(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("travel:location-create")
        data = {
            "name": "",  # невалідне поле — обов’язкове
            "description": "Missing name",
            "city": "Test City",
            "country": self.country.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)
        self.assertIn("This field is required.", form.errors["name"])


class LocationUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Tourist.objects.create_user(
            username="testuser",
            password="password123"
        )
        cls.country = Country.objects.create(name="UA", continent="EU")
        cls.location = Location.objects.create(
            name="Kyiv Castle",
            city="Kyiv",
            description="Historic castle in Kyiv.",
            country=cls.country
        )

    def setUp(self):
        self.client.login(username="testuser", password="password123")

    def test_location_update_view_status_code(self):
        response = self.client.get(
            reverse("travel:location-update",
                    args=[self.location.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "travel/location_form.html")

    def test_location_update_success(self):
        data = {
            "name": "Updated Kyiv Castle",
            "city": "Kyiv",
            "description": "Updated description.",
            "country": self.country.pk
        }
        response = self.client.post(
            reverse("travel:location-update",
                    args=[self.location.pk]),
            data
        )
        self.location.refresh_from_db()
        self.assertRedirects(response, reverse("travel:location-list"))
        self.assertEqual(self.location.name, "Updated Kyiv Castle")


class LocationDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.country = Country.objects.create(
            name="Test Country",
            continent="EU"
        )
        self.location = Location.objects.create(
            name="Test Location",
            description="A test location",
            city="Test City",
            country=self.country,
        )
        self.client.login(username="testuser", password="testpassword")

    def test_delete_location(self):
        url = reverse(
            "travel:location-delete",
            kwargs={"pk": self.location.pk}
        )
        response = self.client.post(url)
        self.assertRedirects(response, reverse("travel:location-list"))
        self.assertFalse(Location.objects.filter(pk=self.location.pk).exists())


class TouristUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            email="old@example.com"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_update_tourist_info(self):
        url = reverse("travel:tourists-update")
        data = {
            "username": "updateduser",
            "email": "updated@example.com",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("travel:tourists-list"))
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
        url = reverse("travel:tourists-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertTemplateUsed(response, "travel/tourist_detail.html")
