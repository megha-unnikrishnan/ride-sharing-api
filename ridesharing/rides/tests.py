from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rides.models import Ride

User = get_user_model()

class RideAPITest(APITestCase):

    def setUp(self):
        """Create a user and a ride before each test"""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)  # Authenticate the user

        self.ride = Ride.objects.create(
            rider=self.user,
            pickup_location="Location X",
            dropoff_location="Location Y",
            status="REQUESTED",
            current_latitude=12.3456,
            current_longitude=78.9012
        )

    def test_get_all_rides(self):
        """Test retrieving all rides"""
        url = reverse("ride-list")  # Ensure you have a URL name 'ride-list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Location X", str(response.data))

    def test_get_single_ride(self):
        """Test retrieving a single ride by ID"""
        url = reverse("ride-detail", kwargs={"pk": self.ride.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pickup_location"], "Location X")

    def test_create_ride(self):
        """Test creating a new ride"""
        url = reverse("ride-list")
        data = {
            "rider": self.user.id,
            "pickup_location": "Location A",
            "dropoff_location": "Location B",
            "status": "REQUESTED",
            "current_latitude": 34.0522,
            "current_longitude": -118.2437
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ride.objects.count(), 2)  # Now there should be 2 rides

    def test_update_ride_status(self):
        """Test updating a ride's status"""
        url = reverse("ride-detail", kwargs={"pk": self.ride.id})
        response = self.client.patch(url, {"status": "COMPLETED"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.status, "COMPLETED")
