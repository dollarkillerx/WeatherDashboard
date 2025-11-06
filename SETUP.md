# Weather Dashboard - Setup Guide

## Prerequisites

### Required Software
- Python 3.8 or higher
- Go 1.24 or higher
- MQTT Broker (Mosquitto recommended)

## Installation

### 1. Install MQTT Broker (Mosquitto)

#### macOS
```bash
brew install mosquitto
brew services start mosquitto
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

#### Windows
Download and install from: https://mosquitto.org/download/

### 2. Python Backend Setup

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Golang Mock Server Setup

```bash
# Download Go dependencies
go mod download
go mod tidy
```

## Running the System

### Step 1: Start MQTT Broker
Make sure Mosquitto is running:

```bash
# Check if Mosquitto is running
# macOS
brew services list | grep mosquitto

# Linux
sudo systemctl status mosquitto

# Or start it manually
mosquitto -v
```

### Step 2: Start Python Flask Backend

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run Flask app
python app.py
```

The Flask backend will:
- Start on http://localhost:5000
- Subscribe to MQTT topic: `weather/data`
- Provide REST API endpoints

### Step 3: Start Golang Mock Data Server

In a new terminal:

```bash
# Run the Golang simulator
go run main.go
```

The Golang server will:
- Connect to MQTT broker at localhost:1883
- Publish weather data every 2 seconds to topic: `weather/data`
- Simulate realistic weather patterns

## API Endpoints

Once the system is running, you can access:

### REST API Endpoints

1. **Health Check**
   ```
   GET http://localhost:5000/api/health
   ```

2. **Current Weather Data**
   ```
   GET http://localhost:5000/api/weather/current
   ```

3. **Historical Weather Data**
   ```
   GET http://localhost:5000/api/weather/history?limit=100
   ```

4. **Weather Statistics**
   ```
   GET http://localhost:5000/api/weather/stats
   ```

## Testing the System

### Test with curl

```bash
# Health check
curl http://localhost:5000/api/health

# Get current weather
curl http://localhost:5000/api/weather/current

# Get history (last 50 readings)
curl http://localhost:5000/api/weather/history?limit=50

# Get statistics
curl http://localhost:5000/api/weather/stats
```

### Test MQTT directly

```bash
# Subscribe to weather data
mosquitto_sub -h localhost -t "weather/data" -v

# In another terminal, the Go server should be publishing
```

## Troubleshooting

### MQTT Connection Issues
- Ensure Mosquitto is running: `mosquitto -v`
- Check if port 1883 is available: `lsof -i :1883` (macOS/Linux)
- Check Mosquitto logs: `tail -f /usr/local/var/log/mosquitto/mosquitto.log` (macOS)

### Python Backend Issues
- Verify dependencies: `pip list | grep -E "Flask|paho-mqtt"`
- Check if port 5000 is available
- Enable debug mode in app.py if needed

### Golang Server Issues
- Verify Go modules: `go mod verify`
- Check MQTT broker connectivity
- Ensure no firewall blocking localhost:1883

## Architecture Flow

```
┌─────────────────────┐
│  Golang Mock Server │
│  (Data Generator)   │
└──────────┬──────────┘
           │
           │ MQTT Protocol
           │ (Publishes to topic)
           ▼
┌─────────────────────┐
│   MQTT Broker       │
│   (Mosquitto)       │
└──────────┬──────────┘
           │
           │ MQTT Protocol
           │ (Subscribes to topic)
           ▼
┌─────────────────────┐
│  Python Flask API   │
│  (Backend)          │
└──────────┬──────────┘
           │
           │ REST API
           │ (HTTP/JSON)
           ▼
┌─────────────────────┐
│  Vue.js Frontend    │
│  (Dashboard)        │
└─────────────────────┘
```

## Development Tips

- The Golang server publishes data every 2 seconds (configurable)
- Flask stores the last 100 readings in memory (configurable)
- All timestamps are in ISO 8601 format
- Weather data uses realistic ranges and smooth transitions

## Next Steps

After setting up Python and Golang components:
1. Develop the Vue.js frontend
2. Create data visualization charts
3. Add real-time updates using WebSocket or polling
4. Implement data persistence (database)
5. Add authentication and user management
