# Ensure Celery is loaded
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ridesharing.settings")

app = Celery("ridesharing")
app.conf.imports = ("rides.tasks",)

app.conf.beat_schedule = {
    "update_rides_every_minute": {
        "task": "rides.tasks.update_ride_locations",
        "schedule": crontab(minute="*"),  # Runs every minute
    }
}
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()