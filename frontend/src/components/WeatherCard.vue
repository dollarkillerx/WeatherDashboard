<template>
  <div class="weather-card">
    <div class="card-header">
      <div class="card-icon">{{ icon }}</div>
      <h3 class="card-title">{{ title }}</h3>
    </div>
    <div class="card-body">
      <div class="card-value">{{ formattedValue }}</div>
      <div class="card-unit">{{ unit }}</div>
    </div>
    <div class="card-footer" v-if="stats">
      <div class="stat">
        <span class="stat-label">Min</span>
        <span class="stat-value">{{ formatNumber(stats.min) }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Avg</span>
        <span class="stat-value">{{ formatNumber(stats.avg) }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Max</span>
        <span class="stat-value">{{ formatNumber(stats.max) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  title: string;
  value: number;
  unit: string;
  icon: string;
  stats?: {
    min: number;
    max: number;
    avg: number;
  };
}

const props = defineProps<Props>();

const formattedValue = computed(() => formatNumber(props.value));

function formatNumber(num: number): string {
  return num.toFixed(1);
}
</script>

<style scoped>
.weather-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 24px;
  color: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.weather-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.card-icon {
  font-size: 32px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.card-body {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 16px;
}

.card-value {
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
}

.card-unit {
  font-size: 24px;
  opacity: 0.8;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  opacity: 0.7;
  text-transform: uppercase;
}

.stat-value {
  font-size: 16px;
  font-weight: 600;
}
</style>
