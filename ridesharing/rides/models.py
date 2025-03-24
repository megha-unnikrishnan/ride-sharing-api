from django.conf import settings
from django.db import models

class Ride(models.Model):
    STATUS_CHOICES = [
        ("REQUESTED", "Requested"),
        ("MATCHED", "Matched"),
        ("ACCEPTED", "Accepted"),
        ("STARTED", "Started"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]


    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rides_requested"
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="rides_driven"
    )
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="REQUESTED")
    created_at = models.DateTimeField(auto_now_add=True)

    
     # New fields for real-time tracking
    current_latitude = models.FloatField(default=0.0, null=False, blank=True)
    current_longitude = models.FloatField(default=0.0, null=False, blank=True)

    def __str__(self):
        return f"Ride {self.id} - {self.pickup_location} to {self.dropoff_location}"
