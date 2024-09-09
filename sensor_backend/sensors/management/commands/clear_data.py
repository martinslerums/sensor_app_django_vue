from django.core.management.base import BaseCommand
from sensors.models import Metric, Unit, MetricUnit, SensorType, SensorVariant, Sensor

class Command(BaseCommand):
    help = 'Clear all records from sensor-related tables'

    def handle(self, *args, **kwargs):
        Metric.objects.all().delete()
        Unit.objects.all().delete()
        MetricUnit.objects.all().delete()
        SensorType.objects.all().delete()
        SensorVariant.objects.all().delete()
        Sensor.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Successfully cleared all sensor data'))
