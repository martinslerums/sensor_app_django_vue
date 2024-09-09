from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from .models import MetricUnit, Sensor, SensorVariant, SensorData
from .serializers import MetricUnitSerializer, SensorSerializer, SensorVariantSerializer
from django.db.models import OuterRef, Subquery, FloatField, Value, Exists, OuterRef, BooleanField, Case, When
from django.db.models.functions import Coalesce


class MetricUnitListView(generics.ListAPIView):
    serializer_class = MetricUnitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['selected']

    def get_queryset(self):
        queryset = MetricUnit.objects.all()
        
        selected = self.request.query_params.get('selected')
        if selected is not None:
            selected = selected.lower() in ['true', '1', 't']
            queryset = queryset.filter(selected=selected)
        
        exclude = self.request.query_params.get('exclude')
        if exclude:
            exclude_ids = [int(id) for id in exclude.split(',') if id.isdigit()]
            queryset = queryset.exclude(id__in=exclude_ids)

        return queryset
    
class SensorFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains') 
    variant_name = CharFilter(field_name='variant__name', lookup_expr='exact')  

    class Meta:
        model = Sensor
        fields = ['name', 'variant_name']

class SensorListView(generics.ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SensorFilter
    ordering_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering', None)

        if ordering:
            metric_id = ordering.lstrip('-')
            if metric_id.isdigit():
                ascending = not ordering.startswith('-')

                queryset = queryset.annotate(
                    metric_value=Coalesce(
                        Subquery(
                            SensorData.objects.filter(
                                sensor=OuterRef('pk'),
                                metric_id=metric_id
                            ).values('value')[:1], 
                            output_field=FloatField()
                        ),
                        Value(float('inf'))
                    ),
                    has_metric_value=Case(
                        When(metric_value=float('inf'), then=Value(True)),
                        default=Value(False),
                        output_field=BooleanField()
                    )
                )

                if ascending:
                    queryset = queryset.order_by('has_metric_value', '-metric_value')
                else:
                    queryset = queryset.order_by('has_metric_value', 'metric_value')

        return queryset

class SensorVariantListView(generics.ListAPIView):
    serializer_class = SensorVariantSerializer

    def get_queryset(self):
        related_sensor_variants = Sensor.objects.filter(variant=OuterRef('pk')).values('variant')

        return SensorVariant.objects.annotate(
            has_related_sensors=Exists(related_sensor_variants)
        ).filter(has_related_sensors=True)
