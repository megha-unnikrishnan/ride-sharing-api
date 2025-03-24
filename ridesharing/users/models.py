from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (('rider', 'Rider'), ('driver', 'Driver'))
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='rider')
    phone_number = models.CharField(max_length=15, blank=True)
    is_available = models.BooleanField(default=False)  # For drivers

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
