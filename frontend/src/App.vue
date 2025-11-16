<template>
  <div class="app">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="header-content">
          <h1 class="app-title">
            <span class="icon">🌤️</span>
            Weather Dashboard
          </h1>
          <div class="header-info">
            <div class="city-selector">
              <label for="city-select">📍 City:</label>
              <select id="city-select" v-model="selectedCity" @change="onCityChange" class="city-select">
                <option v-for="city in cities" :key="city" :value="city">
                  {{ city }}
                </option>
              </select>
            </div>
            <span class="student-code">M24W0295</span>
            <div class="status-indicator" :class="{ connected: isConnected }">
              <span class="status-dot"></span>
              <span class="status-text">{{ connectionStatus }}</span>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main">
      <div class="container">
        <!-- Error Message -->
        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          <span>{{ error }}</span>
          <button @click="retryConnection" class="retry-button">Retry</button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Loading weather data...</p>
        </div>

        <!-- Dashboard Content -->
        <div v-else-if="weatherData" class="dashboard">
          <!-- Weather Cards -->
          <div class="cards-grid">
            <WeatherCard
              title="Temperature"
              :value="weatherData.temperature"
              unit="°C"
              icon="🌡️"
              :stats="stats?.temperature"
            />
            <WeatherCard
              title="Humidity"
              :value="weatherData.humidity"
              unit="%"
              icon="💧"
              :stats="stats?.humidity"
            />
            <WeatherCard
              title="Wind Speed"
              :value="weatherData.wind_speed"
              unit="km/h"
              icon="💨"
              :stats="stats?.wind_speed"
            />
            <WeatherCard
              title="Wind Direction"
              :value="weatherData.wind_direction"
              unit="°"
              icon="🧭"
            />
          </div>

          <!-- Last Updated -->
          <div class="last-updated">
            Last updated: {{ formatLastUpdated(weatherData.last_updated) }}
          </div>

          <!-- Charts -->
          <div class="charts-grid">
            <WeatherChart
              title="Temperature History"
              :labels="chartLabels"
              :datasets="[
                {
                  label: 'Temperature (°C)',
                  data: history.temperature,
                  borderColor: 'rgb(239, 68, 68)',
                  backgroundColor: 'rgba(239, 68, 68, 0.1)',
                },
              ]"
            />
            <WeatherChart
              title="Humidity History"
              :labels="chartLabels"
              :datasets="[
                {
                  label: 'Humidity (%)',
                  data: history.humidity,
                  borderColor: 'rgb(59, 130, 246)',
                  backgroundColor: 'rgba(59, 130, 246, 0.1)',
                },
              ]"
            />
            <WeatherChart
              title="Wind Speed History"
              :labels="chartLabels"
              :datasets="[
                {
                  label: 'Wind Speed (km/h)',
                  data: history.wind_speed,
                  borderColor: 'rgb(16, 185, 129)',
                  backgroundColor: 'rgba(16, 185, 129, 0.1)',
                },
              ]"
            />
          </div>

          <!-- 7-Day Forecast -->
          <div v-if="forecast.length > 0" class="forecast-section">
            <h2 class="forecast-title">7-Day Weather Forecast - {{ selectedCity }}</h2>
            <div class="forecast-grid">
              <div v-for="day in forecast" :key="day.date" class="forecast-card">
                <div class="forecast-date">{{ formatDate(day.date) }}</div>
                <div class="forecast-temps">
                  <span class="temp-max">{{ day.temperature_max.toFixed(1) }}°</span>
                  <span class="temp-separator">/</span>
                  <span class="temp-min">{{ day.temperature_min.toFixed(1) }}°</span>
                </div>
                <div class="forecast-detail">
                  <span>💧 {{ day.humidity.toFixed(0) }}%</span>
                </div>
                <div class="forecast-detail">
                  <span>💨 {{ day.wind_speed.toFixed(1) }} km/h</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <p>Weather Dashboard System - Real-time monitoring via MQTT & REST API</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import WeatherCard from './components/WeatherCard.vue';
import WeatherChart from './components/WeatherChart.vue';
import { weatherApi, type WeatherData, type WeatherHistory, type WeatherStats, type DailyForecast } from './services/weatherApi';

const weatherData = ref<WeatherData | null>(null);
const history = ref<WeatherHistory>({
  temperature: [],
  humidity: [],
  wind_speed: [],
  timestamps: [],
});
const stats = ref<WeatherStats | null>(null);
const forecast = ref<DailyForecast[]>([]);
const cities = ref<string[]>([]);
const selectedCity = ref('Tokyo');
const loading = ref(true);
const error = ref<string | null>(null);
const isConnected = ref(false);
let refreshInterval: number | null = null;

const connectionStatus = computed(() => {
  return isConnected.value ? 'Connected' : 'Disconnected';
});

const chartLabels = computed(() => {
  return history.value.timestamps.map((timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  });
});

function formatLastUpdated(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);

  if (date.toDateString() === today.toDateString()) {
    return 'Today';
  } else if (date.toDateString() === tomorrow.toDateString()) {
    return 'Tomorrow';
  } else {
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    });
  }
}

async function fetchCurrentWeather() {
  try {
    weatherData.value = await weatherApi.getCurrentWeather(selectedCity.value);
    isConnected.value = true;
    error.value = null;
  } catch (err) {
    console.error('Error fetching current weather:', err);
    isConnected.value = false;
    if (!weatherData.value) {
      error.value = 'Failed to fetch weather data. Please ensure the backend is running.';
    }
  }
}

async function fetchWeatherHistory() {
  try {
    history.value = await weatherApi.getWeatherHistory(selectedCity.value, 24);
  } catch (err) {
    console.error('Error fetching weather history:', err);
  }
}

async function fetchWeatherStats() {
  try {
    stats.value = await weatherApi.getWeatherStats(selectedCity.value);
  } catch (err) {
    console.error('Error fetching weather stats:', err);
  }
}

async function fetchWeatherForecast() {
  try {
    forecast.value = await weatherApi.getWeatherForecast(selectedCity.value);
  } catch (err) {
    console.error('Error fetching weather forecast:', err);
  }
}

async function fetchCities() {
  try {
    cities.value = await weatherApi.getCities();
  } catch (err) {
    console.error('Error fetching cities:', err);
    // Fallback to default cities
    cities.value = ['Tokyo', 'Kyoto', 'Osaka', 'Hokkaido', 'New Delhi', 'Beijing', 'Shanghai', 'New York', 'Frankfurt'];
  }
}

async function fetchAllData() {
  await Promise.all([
    fetchCurrentWeather(),
    fetchWeatherHistory(),
    fetchWeatherStats(),
    fetchWeatherForecast(),
  ]);
  loading.value = false;
}

async function retryConnection() {
  error.value = null;
  loading.value = true;
  await fetchAllData();
}

async function onCityChange() {
  // Fetch all data for the newly selected city
  loading.value = true;
  await fetchAllData();
}

function startAutoRefresh() {
  // Refresh data every 30 seconds (Open-Meteo API doesn't update that frequently)
  refreshInterval = window.setInterval(async () => {
    await fetchCurrentWeather();
    await fetchWeatherHistory();
    await fetchWeatherStats();
  }, 30000);
}

function stopAutoRefresh() {
  if (refreshInterval) {
    clearInterval(refreshInterval);
    refreshInterval = null;
  }
}

onMounted(async () => {
  await fetchCities();
  await fetchAllData();
  startAutoRefresh();
});

onBeforeUnmount(() => {
  stopAutoRefresh();
});
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(to bottom, #f1f5f9, #e2e8f0);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  width: 100%;
}

/* Header */
.header {
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.app-title {
  font-size: 28px;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon {
  font-size: 36px;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.city-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
}

.city-select {
  padding: 8px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  outline: none;
}

.city-select:hover {
  border-color: #667eea;
}

.city-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.student-code {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 14px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  background: #fee;
  color: #dc2626;
  font-size: 14px;
  font-weight: 600;
}

.status-indicator.connected {
  background: #efe;
  color: #16a34a;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Main Content */
.main {
  flex: 1;
  padding: 32px 0;
}

/* Error Message */
.error-message {
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #dc2626;
}

.error-icon {
  font-size: 24px;
}

.retry-button {
  margin-left: auto;
  background: #dc2626;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-button:hover {
  background: #b91c1c;
}

/* Loading */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  gap: 16px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Dashboard */
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.last-updated {
  text-align: center;
  color: #64748b;
  font-size: 14px;
  font-style: italic;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

/* Forecast Section */
.forecast-section {
  margin-top: 32px;
}

.forecast-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 20px;
  text-align: center;
}

.forecast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
}

.forecast-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s;
}

.forecast-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.forecast-date {
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 12px;
  font-size: 14px;
}

.forecast-temps {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 12px;
}

.temp-max {
  color: #ef4444;
}

.temp-separator {
  color: #94a3b8;
  margin: 0 4px;
}

.temp-min {
  color: #3b82f6;
}

.forecast-detail {
  font-size: 13px;
  color: #64748b;
  margin-top: 6px;
}

/* Footer */
.footer {
  background: white;
  border-top: 1px solid #e2e8f0;
  padding: 20px 0;
  text-align: center;
  color: #64748b;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .app-title {
    font-size: 24px;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
