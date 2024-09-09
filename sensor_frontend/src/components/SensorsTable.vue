<template>
  <div class="sensor-container">
    <div class="sensor-table-actions-wrapper">
      <div class="search-filter-wrapper">
        <CustomInput
          v-model="searchQueryName"
          @enter="getSensors"
          placeholder="Press Enter"
        />
        <CustomSelect
          v-model="searchQueryVariant"
          :options="
            sensorVariants.map((variant) => ({
              id: variant.id,
              value: variant.name,
              text: variant.name,
            }))
          "
          placeholder="Select a type"
          @change="onTypeChange"
        />
      </div>

      <div class="checkbox-wrapper">
        <CustomCheckbox
          v-for="metric in allMetrics"
          :key="metric.metric.id"
          :value="metric.metric.id"
          :checked="!excludedMetrics.includes(metric.metric.id)"
          :label="metric.metric.name"
          @change="toggleExcludeMetric"
        />
      </div>
    </div>

    <table class="sensor-table">
      <thead>
        <tr>
          <th>
            <div class="sortable-header" @click="sortByColumn('name')">
              Sensor Name
              <span class="sort-icon">
                <span v-if="sortColumn === 'name'">
                  {{
                    sortOrder === "asc" ? "↑" : sortOrder === "desc" ? "↓" : "↕"
                  }}
                </span>
                <span v-else> ↕ </span>
              </span>
            </div>
          </th>
          <th v-for="metric in activeMetrics" :key="metric.metric.id">
            <div
              class="sortable-header"
              @click="sortByColumn(metric.metric.id)"
            >
              {{ metric.metric.name }} [{{ metric.unit.name }}]
              <span class="sort-icon">
                <span v-if="sortColumn === metric.metric.id">
                  {{
                    sortOrder === "asc" ? "↑" : sortOrder === "desc" ? "↓" : "↕"
                  }}
                </span>
                <span v-else> ↕ </span>
              </span>
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sensor in sensors" :key="sensor.id">
          <td>
            <p>{{ sensor.name }}</p>
            <p class="sensor_id">ID: {{ sensor.id }}</p>
          </td>
          <td v-for="metric in activeMetrics" :key="metric.metric.id">
            <span
              v-if="
                sensor.metrics && sensor.metrics[metric.metric.id] !== undefined
              "
            >
              {{ sensor.metrics[metric.metric.id].v }}
            </span>
            <div v-else class="no-data">-</div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import API from "../axios";
import CustomInput from "./CustomInput.vue";
import CustomSelect from "./CustomSelect.vue";
import CustomCheckbox from "./CustomCheckbox.vue";
import { Sensor, UnitMetric, SensorVariant } from "../typings/types";

const sensors = ref<Sensor[]>([]);
const allMetrics = ref<UnitMetric[]>([]);
const activeMetrics = ref<UnitMetric[]>([]);
const excludedMetrics = ref<number[]>([]);
const sensorVariants = ref<SensorVariant[]>([]);

const searchQueryName = ref("");
const searchQueryVariant = ref("");

const sortColumn = ref<string | number | null>(null);
const sortOrder = ref<"asc" | "desc" | null>(null);

onMounted(async () => {
  await Promise.all([getMetrics(), getSensors(), getSensorVariants()]);
});

const getSensors = async () => {
  try {
    const params: any = {};

    if (searchQueryName.value) {
      params.name = searchQueryName.value;
    }

    if (searchQueryVariant.value) {
      params.variant_name = searchQueryVariant.value;
    }

    if (sortColumn.value) {
      params.ordering =
        sortOrder.value === "asc"
          ? `${sortColumn.value}`
          : `-${sortColumn.value}`;
    }

    const response = await API.get("/sensors/", { params });

    if (response.data.length > 0) {
      sensors.value = response.data;
    }
  } catch (error) {
    console.error("Error fetching sensors data:", error);
  }
};

const getMetrics = async () => {
  try {
    const response = await API.get("/metric-units/", {
      params: { selected: true },
    });

    if (response.data.length > 0) {
      allMetrics.value = response.data;
      updateActiveMetrics();
    }
  } catch (error) {
    console.error("Error fetching metrics data:", error);
  }
};

const getSensorVariants = async () => {
  try {
    const response = await API.get("/sensor-variants/");
    if (response.data.length > 0) {
      sensorVariants.value = response.data;
    }
  } catch (error) {
    console.error("Error fetching sensor variants data:", error);
  }
};

const sortByColumn = (column: string | number) => {
  if (column === sortColumn.value) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : null;
    sortColumn.value = sortOrder.value === null ? null : sortColumn.value;
  } else {
    sortColumn.value = column;
    sortOrder.value = "asc";
  }

  getSensors();
};

const onTypeChange = (value: string) => {
  searchQueryVariant.value = value;
  getSensors();
};

const updateActiveMetrics = () => {
  activeMetrics.value = allMetrics.value.filter(
    (metric: UnitMetric) => !excludedMetrics.value.includes(metric.metric.id)
  );
};

const toggleExcludeMetric = (metricID: number) => {
  excludedMetrics.value.includes(metricID)
    ? (excludedMetrics.value = excludedMetrics.value.filter(
        (id) => id !== metricID
      ))
    : excludedMetrics.value.push(metricID);

  updateActiveMetrics();
};
</script>

<style scoped>
.sensor-container {
  padding: 1.2rem;
}

.sensor-table-actions-wrapper {
  display: flex;
  gap: 2rem; 
}

.search-filter-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem; 
}

.checkbox-wrapper {
  display: grid;
  width: 100%;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

@media (max-width: 600px) {
  .checkbox-wrapper {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
}

.sensor-table {
  width: 100%;
  margin-top: 1rem;
  border-collapse: collapse;
}

.sensor-table th,
.sensor-table td {
  border: 1px solid #ddd;
  padding: 0.3rem;
  text-align: center;
  font-size: 12px;
}

.sensor-table th {
  background-color: #f4f4f4;
}

.th_metric {
  display: flex;
}

.sensor_id {
  font-size: 10px;
  color: lightgray;
}

.sortable-header {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.sort-icon {
  margin-left: 5px;
  font-size: 12px;
  color: #555;
}

</style>
