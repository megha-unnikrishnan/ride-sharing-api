from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ride
from .serializers import RideSerializer, RideStatusUpdateSerializer  # Import missing serializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Update the status of a ride (e.g., started, completed, cancelled).
        """
        ride = self.get_object()
        serializer = RideStatusUpdateSerializer(ride, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Ride status updated to {ride.status}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated], url_path='match-driver')
    def match_driver(self, request, pk=None):
        ride = self.get_object()
        User = get_user_model()

        try:
            drivers_group = Group.objects.get(name="Drivers")
        except Group.DoesNotExist:
            return Response({'message': 'Drivers group not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Debug: Print all drivers in the group
        all_drivers = User.objects.filter(groups=drivers_group)
        print("All drivers:", [(driver.username, driver.is_available) for driver in all_drivers])

        # Find available driver
        available_driver = all_drivers.filter(is_available=True).exclude(rides_driven__status="STARTED").first()

        if not available_driver:
            return Response({'message': 'No available drivers found'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            ride.driver = available_driver
            ride.status = 'MATCHED'
            ride.save()
            available_driver.is_available = False
            available_driver.save()

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
