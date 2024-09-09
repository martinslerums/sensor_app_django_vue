<template>
  <div class="custom-select-container">
    <select
      :value="modelValue"
      @change="handleChange"
      class="custom-select"
    >
      <option value="">{{ placeholder }}</option>
      <option
        v-for="option in options"
        :key="option.id"
        :value="option.value"
      >
        {{ option.text }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">

defineProps<{
  modelValue: string;
  options: { id: string | number; value: string; text: string }[];
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
  (e: 'change', value: string): void;
}>();

const handleChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  const newValue = target.value || '';

  emit('update:modelValue', newValue);
  emit('change', newValue); 
};
</script>

<style scoped>
.custom-select-container {
  margin: 0.5rem 0;
}

.custom-select {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.12);
  transition: border-color 0.2s ease-in-out;
}

.custom-select:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(0, 0, 0, 0.25);
}
</style>
