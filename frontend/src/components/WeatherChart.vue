<template>
  <div class="chart-container">
    <h3 class="chart-title">{{ title }}</h3>
    <div class="chart-wrapper">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
  Filler,
  type ChartConfiguration,
} from 'chart.js';

// Register Chart.js components
Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface Props {
  title: string;
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    borderColor: string;
    backgroundColor: string;
  }[];
}

const props = defineProps<Props>();
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

function createChart() {
  if (!chartCanvas.value) return;

  const config: ChartConfiguration = {
    type: 'line',
    data: {
      labels: props.labels,
      datasets: props.datasets.map((dataset) => ({
        ...dataset,
        tension: 0.4,
        fill: true,
        pointRadius: 3,
        pointHoverRadius: 6,
        borderWidth: 2,
      })),
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index',
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            color: '#64748b',
            font: {
              size: 12,
              weight: '600',
            },
            usePointStyle: true,
            padding: 15,
          },
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          padding: 12,
          cornerRadius: 8,
          displayColors: true,
        },
      },
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            color: '#94a3b8',
            maxTicksLimit: 10,
            font: {
              size: 11,
            },
          },
        },
        y: {
          grid: {
            color: 'rgba(148, 163, 184, 0.1)',
          },
          ticks: {
            color: '#94a3b8',
            font: {
              size: 11,
            },
          },
        },
      },
    },
  };

  chartInstance = new Chart(chartCanvas.value, config);
}

function updateChart() {
  if (!chartInstance) return;

  chartInstance.data.labels = props.labels;
  chartInstance.data.datasets = props.datasets.map((dataset) => ({
    ...dataset,
    tension: 0.4,
    fill: true,
    pointRadius: 3,
    pointHoverRadius: 6,
    borderWidth: 2,
  }));
  chartInstance.update('none');
}

onMounted(() => {
  createChart();
});

watch(
  () => [props.labels, props.datasets],
  () => {
    updateChart();
  },
  { deep: true }
);

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
.chart-container {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.chart-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 20px 0;
}

.chart-wrapper {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>
