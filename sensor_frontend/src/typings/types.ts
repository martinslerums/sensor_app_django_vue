type Metric = { id: number; name: string };
type Unit = { id: number; name: string; precision: number };

export type UnitMetric = {
  id: number;
  metric: Metric;
  unit: Unit;
  selected: boolean;
};

export type Sensor = {
  id: number;
  name: string;
  sensor_type: number;
  variant: SensorVariant;
  metrics?: Record<number, { t: string; v: number }>;
};

export type SensorVariant = {
  id: number;
  name: string;
  variant_code: number;
};
