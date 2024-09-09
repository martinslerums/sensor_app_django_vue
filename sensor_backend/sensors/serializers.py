from rest_framework import serializers
from .models import Metric, Unit, MetricUnit, Sensor, SensorData, SensorType, SensorVariant


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'

class MetricUnitSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    metric = MetricSerializer(read_only=True)

    class Meta:
        model = MetricUnit
        fields = [ 'metric', 'unit', 'selected']

class MetricValueSerializer(serializers.Serializer):
    t = serializers.DateTimeField(source='timestamp')
    v = serializers.FloatField(source='value')

class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = '__all__'

class SensorVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorVariant
        fields = ['id', 'name', 'variant_code']

class SensorSerializer(serializers.ModelSerializer):
    sensor_type = serializers.PrimaryKeyRelatedField(read_only=True) 
    variant = SensorVariantSerializer(read_only=True)
    metrics = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'sensor_type', 'variant', 'metrics']

    def get_metrics(self, obj):
        sensor_data = SensorData.objects.filter(sensor=obj)
        metrics = {}
        for data in sensor_data:
            metrics[data.metric.id] = MetricValueSerializer(data).data
        return metrics


