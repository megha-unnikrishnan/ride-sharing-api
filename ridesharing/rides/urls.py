from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet,update_ride_location

router = DefaultRouter()
router.register(r'', RideViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:ride_id>/update-location/', update_ride_location, name='update_ride_location'),
]

