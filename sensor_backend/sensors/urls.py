from django.urls import path
from .views import MetricUnitListView, SensorListView, SensorVariantListView

urlpatterns = [
    path('sensors/', SensorListView.as_view(), name='sensor-list'),
    path('sensor-variants/', SensorVariantListView.as_view(), name='sensor-variant-list'),
    path('metric-units/', MetricUnitListView.as_view(), name='metric-unit-list'),
]
