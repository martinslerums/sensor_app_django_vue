import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from sensors.models import SensorType, SensorVariant, Metric, Unit, MetricUnit, Sensor, SensorData

class Command(BaseCommand):
    help = 'Import sensor data from JSON files into the database'

    def handle(self, *args, **kwargs):
        with open('data/sensorTypes.json') as f:
            sensor_types_data = json.load(f)

        for type_id, variants in sensor_types_data.items():
            sensor_type, created = SensorType.objects.get_or_create(id=type_id)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created SensorType with ID {type_id}.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'SensorType with ID {type_id} already exists.'))

            for variant_id, variant_info in variants.items():
                SensorVariant.objects.get_or_create(
                    sensor_type=sensor_type,
                    variant_code=variant_id,
                    defaults={'name': variant_info.get('name', 'Unknown_variant')}
                )
                self.stdout.write(self.style.SUCCESS(f'Created/Updated SensorVariant with code {variant_id} for SensorType ID {type_id}.'))

        with open('data/metrics.json') as f:
            metrics_data = json.load(f)

        metrics = metrics_data['data']['items']
        for metric_data in metrics:
            metric_id = int(metric_data['id'])
            metric_name = metric_data.get('name', 'Unknown_metric')
            Metric.objects.get_or_create(id=metric_id, defaults={'name': metric_name})
            self.stdout.write(self.style.SUCCESS(f'Created/Updated Metric with ID {metric_id}.'))
            
            for unit_data in metric_data.get('units', []):
                unit_id = int(unit_data['id'])
                unit_name = unit_data.get('name', 'Unknown_unit')
                unit_precision = int(unit_data.get('precision', 0))
                unit, created = Unit.objects.get_or_create(id=unit_id, defaults={'name': unit_name, 'precision': unit_precision})
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created Unit with ID {unit_id}.'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Unit with ID {unit_id} already exists.'))
                
                MetricUnit.objects.get_or_create(
                    metric_id=metric_id,
                    unit_id=unit_id,
                    defaults={'selected': unit_data.get('selected', False)}
                )
                self.stdout.write(self.style.SUCCESS(f'Created/Updated MetricUnit for Metric ID {metric_id} and Unit ID {unit_id}.'))

        with open('data/sensors.json') as f:
            sensors_data = json.load(f)

        for sensor_id, sensor_info in sensors_data.items():
            sensor_type_id = sensor_info.get('type')
            sensor_variant_code = sensor_info.get('variant')

            try:
                sensor_type = SensorType.objects.get(id=sensor_type_id)
            except SensorType.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'SensorType with ID {sensor_type_id} does not exist. Skipping sensor {sensor_id}.'))
                continue

            try:
                sensor_variant = SensorVariant.objects.get(sensor_type=sensor_type, variant_code=sensor_variant_code)
            except SensorVariant.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'SensorVariant with code {sensor_variant_code} for SensorType ID {sensor_type_id} does not exist. Skipping sensor {sensor_id}.'))
                continue

            sensor, created = Sensor.objects.get_or_create(
                id=sensor_id,  
                defaults={'name': sensor_info.get('name', 'Unknown_sensor'), 'sensor_type': sensor_type, 'variant': sensor_variant}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Sensor with ID {sensor_id}.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Sensor with ID {sensor_id} already exists.'))


            for metric_id, metric_info in sensor_info.get('metrics', {}).items():
                try:
                    metric = Metric.objects.get(id=int(metric_id))
                except Metric.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Metric with ID {metric_id} does not exist. Skipping data for sensor {sensor_id}.'))
                    continue

                timestamp = timezone.make_aware(datetime.fromtimestamp(metric_info['t']))
                value = metric_info['v']
                
                SensorData.objects.update_or_create(
                    sensor=sensor,
                    metric=metric,
                    timestamp=timestamp,
                    defaults={'value': value}
                )
                self.stdout.write(self.style.SUCCESS(f'Created/Updated SensorData for Sensor ID {sensor_id}, Metric ID {metric_id}, Timestamp {timestamp}.'))

        self.stdout.write(self.style.SUCCESS('Successfully imported sensor data from JSON files.'))
