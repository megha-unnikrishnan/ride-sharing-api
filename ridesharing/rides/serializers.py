from rest_framework import serializers
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
class RideStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["status"]

    def validate_status(self, value):
        """Ensure the status update follows logical flow"""
        valid_statuses = dict(Ride.STATUS_CHOICES).keys()  # Extract valid keys
        if value.upper() not in valid_statuses:  # Convert input to uppercase
            raise serializers.ValidationError("Invalid status update.")

        current_status = self.instance.status
        if current_status == "COMPLETED":
            raise serializers.ValidationError("Ride is already completed.")
        if current_status == "CANCELLED":
            raise serializers.ValidationError("Ride is already cancelled.")
        if current_status == "REQUESTED" and value.upper() == "COMPLETED":
            raise serializers.ValidationError("Ride must start before being completed.")

        return value.upper()  # Normalize input to uppercase



class RideMatchSerializer(serializers.ModelSerializer):
    driver_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ride
        fields = ['driver_id', 'status']

    def update(self, instance, validated_data):
        instance.driver = validated_data.get('driver_id')
        instance.status = 'matched'
        instance.save()
        return instance