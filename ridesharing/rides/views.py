from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ride
from .serializers import RideSerializer, RideStatusUpdateSerializer  # Import missing serializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated], url_path='match-driver')
    def match_driver(self, request, pk=None):
        """
        Match a ride request with an available driver based on some criteria.
        """
        ride = self.get_object()
        User = get_user_model()

        # Find the first available driver who is NOT already on a ride
        available_driver = User.objects.filter(user_type='driver', is_available=True).exclude(rides_driven__status="STARTED").first()

        if not available_driver:
            return Response({'message': 'No available drivers found'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():  # Ensures database consistency
            ride.driver = available_driver
            ride.status = 'MATCHED'
            ride.save()

            available_driver.is_available = False  # Mark driver as busy
            available_driver.save()

        return Response({'message': f'Ride {ride.id} matched with driver {ride.driver.username}'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated], url_path='match-driver')
    def match_driver(self, request, pk=None):
        """
        Match a ride request with an available driver.
        """
        ride = self.get_object()
        User = get_user_model()

        # Find available drivers from the "Drivers" group
        drivers_group = Group.objects.get(name="Drivers")
        available_driver = User.objects.filter(groups=drivers_group, rides_driven__isnull=True).first()

        if not available_driver:
            return Response({'message': 'No available drivers found'}, status=status.HTTP_400_BAD_REQUEST)

        # Assign the driver and update status
        ride.driver = available_driver
        ride.status = 'matched'
        ride.save()
        return Response({'message': f'Ride {ride.id} matched with driver {ride.driver.username}'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated], url_path='accept-ride')
    def accept_ride(self, request, pk=None):
        """
        Allow a driver to accept a ride.
        """
        ride = self.get_object()

        # Ensure only the assigned driver can accept
        if ride.driver != request.user:
            return Response({'message': 'You are not assigned to this ride'}, status=status.HTTP_403_FORBIDDEN)

        # Update ride status to accepted
        ride.status = 'ACCEPTED'
        ride.save()
        return Response({'message': f'Driver {request.user.username} accepted the ride'}, status=status.HTTP_200_OK)
    
from rest_framework.decorators import api_view, permission_classes
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_ride_location(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id, driver=request.user)
        if ride.status != "STARTED":
            return Response({"message": "Ride is not ongoing"})
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if latitude and longitude:
            ride.current_latitude = latitude
            ride.current_longitude = longitude
            ride.save()
            return Response({"message": "Location updated successfully!"})
        return Response({"error": "Latitude and longitude required"}, status=400)

    except Ride.DoesNotExist:
        return Response({"error": "Ride not found or unauthorized"}, status=404)