from celery import shared_task
from .models import Ride
import logging

logger = logging.getLogger(__name__)

@shared_task(name="rides.tasks.update_ride_locations")
def update_ride_locations():
    """
    Updates the location of all active rides every minute.
    """
    try:
        rides = Ride.objects.filter(status="STARTED")
        updated_count = 0

        for ride in rides:
            # Simulate location updates (Modify logic if necessary)
            ride.current_latitude += 5  
            ride.current_longitude += 5  
            ride.save()
            updated_count += 1

        logger.info(f"Updated {updated_count} ride locations.")
        return f"Updated {updated_count} ride locations."

    except Exception as e:
        logger.error(f"Error updating ride locations: {e}")
        return f"Error updating ride locations: {e}"
