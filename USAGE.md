# Weather Dashboard - Usage Guide

## Overview

The Weather Dashboard has been updated to use real weather data from **Open-Meteo API** instead of mock data. The system now supports multiple cities and provides 7-day weather forecasts.

## New Features

### 1. Real Weather Data
- **Current Weather**: Real-time data from Open-Meteo API
- **7-Day Forecast**: Daily forecasts for the next 7 days
- **Multiple Cities**: Support for 9 major cities worldwide

### 2. Supported Cities

1. **Tokyo** (東京) - Japan
2. **Kyoto** (京都) - Japan
3. **Osaka** (大阪) - Japan
4. **Hokkaido** (北海道) - Japan
5. **New Delhi** (नई दिल्ली) - India
6. **Beijing** (北京) - China
7. **Shanghai** (上海) - China
8. **New York** - USA
9. **Frankfurt** - Germany

### 3. API Endpoints

#### New Endpoints
- `GET /api/weather/forecast?city=Tokyo` - Get 7-day forecast for a specific city
- `GET /api/cities` - Get list of available cities

#### Existing Endpoints
- `GET /api/health` - Health check
- `GET /api/weather/current` - Get current weather (from MQTT stream)
- `GET /api/weather/history?limit=100` - Get historical weather data
- `GET /api/weather/stats` - Get weather statistics

## How to Run

### 1. Start MQTT Broker
```bash
# Using Docker
docker run -it -p 1883:1883 eclipse-mosquitto:latest

# Or using mosquitto directly
mosquitto -p 1883
```

### 2. Start Go Weather Data Provider
```bash
# Build
go build -o weather-server main.go

# Run
./weather-server
```

The Go service will:
- Fetch real weather data from Open-Meteo API
- Publish data to MQTT broker every 10 seconds
- Default city: Tokyo

### 3. Start Flask API Server
```bash
# Install dependencies
pip install flask flask-cors paho-mqtt requests

# Run server
python3 app.py
```

The Flask server will:
- Subscribe to MQTT weather data
- Provide REST API endpoints
- Serve 7-day forecasts from Open-Meteo API

### 4. Start Frontend
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Access the dashboard at: http://localhost:5173

## Using the Dashboard

### City Selection
1. Click the city dropdown in the header (📍 City)
2. Select any of the 9 available cities
3. The 7-day forecast will update automatically

### Dashboard Features

#### Current Weather Cards
- **Temperature** - Real-time temperature in °C
- **Humidity** - Current humidity percentage
- **Wind Speed** - Current wind speed in km/h
- **Wind Direction** - Wind direction in degrees

#### Historical Charts
- Temperature, humidity, and wind speed trends
- Real-time updates every 2 seconds
- Last 50 data points displayed

#### 7-Day Forecast
- Daily temperature range (max/min)
- Average humidity
- Maximum wind speed
- Shows "Today", "Tomorrow", then weekday names

## Technical Details

### Go Service Changes
- **Before**: Generated random mock data
- **After**: Fetches real data from Open-Meteo API
- **Interval**: Updates every 10 seconds (configurable)

### Flask API Changes
- Added `requests` library for HTTP calls
- New city coordinates mapping
- New `/api/weather/forecast` endpoint
- New `/api/cities` endpoint

### Frontend Changes
- Added city selector dropdown
- Added 7-day forecast display
- New API methods in `weatherApi.ts`
- Responsive forecast cards with hover effects

## Testing

### Test Open-Meteo API Integration
```bash
python3 test_openmeteo.py
```

Expected output:
```
✓ Successfully fetched current weather
✓ Successfully fetched 7-day forecast
✓ All tests passed!
```

### Test Flask API
```bash
# Get cities
curl http://localhost:5000/api/cities

# Get forecast for Tokyo
curl http://localhost:5000/api/weather/forecast?city=Tokyo

# Get forecast for New York
curl "http://localhost:5000/api/weather/forecast?city=New%20York"
```

## Architecture

```
┌──────────────────┐
│  Open-Meteo API  │
└────────┬─────────┘
         │ HTTP
         ↓
┌──────────────────┐     MQTT      ┌──────────────────┐
│   Go Service     │─────────────→ │  MQTT Broker     │
│ (Weather Data)   │               │  (mosquitto)     │
└──────────────────┘               └─────────┬────────┘
                                             │ MQTT
         ↓ HTTP (7-day forecast)             ↓
┌──────────────────┐               ┌──────────────────┐
│  Open-Meteo API  │               │   Flask API      │
└────────┬─────────┘               │   (Backend)      │
         │                         └─────────┬────────┘
         │                                   │ REST API
         └───────────────────────────────────┘
                                             │ HTTP
                                             ↓
                                   ┌──────────────────┐
                                   │  Vue.js Frontend │
                                   │   (Dashboard)    │
                                   └──────────────────┘
```

## Notes

- Open-Meteo API is free and doesn't require an API key
- Data updates are based on MQTT publish interval (10 seconds for Go service)
- 7-day forecasts are fetched on-demand when city is selected
- Historical data is stored in-memory (last 100 readings)

## Troubleshooting

### No weather data in dashboard
1. Check if MQTT broker is running: `netstat -an | grep 1883`
2. Check if Go service is connected to MQTT
3. Check Flask server logs for MQTT connection

### Forecast not loading
1. Check internet connection (Open-Meteo API requires internet)
2. Check browser console for API errors
3. Test API endpoint directly: `curl http://localhost:5000/api/weather/forecast?city=Tokyo`

### City not found error
1. Ensure city name matches exactly (case-sensitive)
2. Use `/api/cities` endpoint to get valid city names
3. Check that city is in the CITIES dictionary
