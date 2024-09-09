<template>
  <div class="custom-input-container">
    <input
      :value="modelValue"
      @input="onInput"
      @keyup.enter="onEnter"
      :placeholder="placeholder"
      class="custom-input"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "enter"): void;
}>();

const onInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit("update:modelValue", target.value);
};

const onEnter = (event: KeyboardEvent) => {
  if (event.key === "Enter") {
    emit("enter");
  }
};
</script>

<style scoped>
.custom-input-container {
  margin: 0.5rem 0;
}

.custom-input {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.12);
  transition: border-color 0.2s ease-in-out;
}

.custom-input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 0 0.2rem rgba(0, 0, 0, 0.25);
}
</style>
