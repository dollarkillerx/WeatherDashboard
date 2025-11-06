import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

export interface WeatherData {
  temperature: number;
  humidity: number;
  wind_direction: number;
  wind_speed: number;
  last_updated: string;
}

export interface WeatherHistory {
  temperature: number[];
  humidity: number[];
  wind_speed: number[];
  timestamps: string[];
}

export interface WeatherStats {
  temperature: {
    current: number;
    min: number;
    max: number;
    avg: number;
  };
  humidity: {
    current: number;
    min: number;
    max: number;
    avg: number;
  };
  wind_speed: {
    current: number;
    min: number;
    max: number;
    avg: number;
  };
}

export interface ApiResponse<T> {
  status: string;
  data: T;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const weatherApi = {
  /**
   * Health check endpoint
   */
  async healthCheck() {
    const response = await api.get('/api/health');
    return response.data;
  },

  /**
   * Get current weather data
   */
  async getCurrentWeather(): Promise<WeatherData> {
    const response = await api.get<ApiResponse<WeatherData>>('/api/weather/current');
    return response.data.data;
  },

  /**
   * Get weather history
   * @param limit - Number of historical records to retrieve (default: 100)
   */
  async getWeatherHistory(limit: number = 100): Promise<WeatherHistory> {
    const response = await api.get<ApiResponse<WeatherHistory>>('/api/weather/history', {
      params: { limit },
    });
    return response.data.data;
  },

  /**
   * Get weather statistics
   */
  async getWeatherStats(): Promise<WeatherStats> {
    const response = await api.get<ApiResponse<WeatherStats>>('/api/weather/stats');
    return response.data.data;
  },
};

export default weatherApi;
