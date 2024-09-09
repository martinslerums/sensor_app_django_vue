<template>
  <label class="custom-checkbox-label">
    <input
      type="checkbox"
      :value="value"
      :checked="checked"
      @change="handleChange"
      class="custom-checkbox-input"
    />
    <span class="custom-checkbox-text">{{ label }}</span>
  </label>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps<{
  value: number;
  checked: boolean;
  label: string;
}>();

const emit = defineEmits<{
  (e: 'change', value: number): void;
}>();

const handleChange = () => {
  emit('change', props.value);
};
</script>

<style scoped>
.custom-checkbox-label {
  display: flex;
  align-items: center;
}

.custom-checkbox-input {
  margin-right: 0.5rem;
}

.custom-checkbox-text {
  font-size: 0.9rem;
  font-weight: 500;
}
</style>
