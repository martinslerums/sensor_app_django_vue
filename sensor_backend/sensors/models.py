from django.db import models


class Metric(models.Model):
    name = models.CharField(max_length=100, blank=True, default='n/a')

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50, blank=True, default='n/a')
    precision = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class MetricUnit(models.Model):
    metric = models.ForeignKey(Metric, related_name='metric_units', on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, related_name='unit_metrics', on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)

    class Meta:
        unique_together = ('metric', 'unit')

class SensorType(models.Model):
    def __str__(self):
        return str(self.id) 

class SensorVariant(models.Model):
    sensor_type = models.ForeignKey(SensorType, related_name='variants', on_delete=models.CASCADE)
    variant_code = models.IntegerField(default=0)
    name = models.CharField(max_length=100, blank=True, default='n/a')

    def __str__(self):
        return f"{self.sensor_type.id}-{self.variant_code}" 

class Sensor(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True, default='n/a')
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)  
    variant = models.ForeignKey(SensorVariant, on_delete=models.CASCADE)  

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = 'n/a'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='data', on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.sensor.name} - {self.metric.name} at {self.timestamp}"
