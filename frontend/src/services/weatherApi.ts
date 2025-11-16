import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001';

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

export interface DailyForecast {
  date: string;
  temperature_max: number;
  temperature_min: number;
  humidity: number;
  wind_speed: number;
  wind_direction: number;
}

export interface ApiResponse<T> {
  status: string;
  data: T;
  city?: string;
  cities?: string[];
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
   * @param city - City name (default: Tokyo)
   */
  async getCurrentWeather(city: string = 'Tokyo'): Promise<WeatherData> {
    const response = await api.get<ApiResponse<WeatherData>>('/api/weather/current', {
      params: { city },
    });
    return response.data.data;
  },

  /**
   * Get weather history
   * @param city - City name (default: Tokyo)
   * @param limit - Number of historical records to retrieve (default: 24)
   */
  async getWeatherHistory(city: string = 'Tokyo', limit: number = 24): Promise<WeatherHistory> {
    const response = await api.get<ApiResponse<WeatherHistory>>('/api/weather/history', {
      params: { city, limit },
    });
    return response.data.data;
  },

  /**
   * Get weather statistics
   * @param city - City name (default: Tokyo)
   */
  async getWeatherStats(city: string = 'Tokyo'): Promise<WeatherStats> {
    const response = await api.get<ApiResponse<WeatherStats>>('/api/weather/stats', {
      params: { city },
    });
    return response.data.data;
  },

  /**
   * Get 7-day weather forecast for a city
   * @param city - City name
   */
  async getWeatherForecast(city: string = 'Tokyo'): Promise<DailyForecast[]> {
    const response = await api.get<ApiResponse<DailyForecast[]>>('/api/weather/forecast', {
      params: { city },
    });
    return response.data.data;
  },

  /**
   * Get list of available cities
   */
  async getCities(): Promise<string[]> {
    const response = await api.get<ApiResponse<string[]>>('/api/cities');
    return response.data.cities || [];
  },
};

export default weatherApi;
