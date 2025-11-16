package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

// WeatherData represents the weather metrics being simulated
type WeatherData struct {
	Temperature   float64 `json:"temperature"`
	Humidity      float64 `json:"humidity"`
	WindDirection float64 `json:"wind_direction"`
	WindSpeed     float64 `json:"wind_speed"`
	Timestamp     string  `json:"timestamp"`
}

// OpenMeteoResponse represents the response from Open-Meteo API
type OpenMeteoResponse struct {
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
	Current   struct {
		Time          string  `json:"time"`
		Temperature   float64 `json:"temperature_2m"`
		Humidity      float64 `json:"relative_humidity_2m"`
		WindSpeed     float64 `json:"wind_speed_10m"`
		WindDirection float64 `json:"wind_direction_10m"`
	} `json:"current"`
}

// City represents a city with its coordinates
type City struct {
	Name      string
	Latitude  float64
	Longitude float64
}

var cities = map[string]City{
	"Tokyo":       {Name: "Tokyo", Latitude: 35.6895, Longitude: 139.6917},
	"Kyoto":       {Name: "Kyoto", Latitude: 35.0116, Longitude: 135.7681},
	"Osaka":       {Name: "Osaka", Latitude: 34.6937, Longitude: 135.5023},
	"Hokkaido":    {Name: "Hokkaido", Latitude: 43.0642, Longitude: 141.3469},
	"New Delhi":   {Name: "New Delhi", Latitude: 28.6139, Longitude: 77.2090},
	"Beijing":     {Name: "Beijing", Latitude: 39.9042, Longitude: 116.4074},
	"Shanghai":    {Name: "Shanghai", Latitude: 31.2304, Longitude: 121.4737},
	"New York":    {Name: "New York", Latitude: 40.7128, Longitude: -74.0060},
	"Frankfurt":   {Name: "Frankfurt", Latitude: 50.1109, Longitude: 8.6821},
}

// Configuration constants
const (
	MQTTBroker        = "tcp://localhost:1883"
	MQTTTopic         = "weather/data"
	PublishInterval   = 10 * time.Second // Fetch real data every 10 seconds
	ClientID          = "golang-weather-provider"
	DefaultCity       = "Tokyo"
	OpenMeteoAPI      = "https://api.open-meteo.com/v1/forecast"
)

var currentCity = DefaultCity

// fetchWeatherFromOpenMeteo fetches real weather data from Open-Meteo API
func fetchWeatherFromOpenMeteo(city City) (*WeatherData, error) {
	url := fmt.Sprintf("%s?latitude=%.4f&longitude=%.4f&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m",
		OpenMeteoAPI, city.Latitude, city.Longitude)

	resp, err := http.Get(url)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch weather data: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %v", err)
	}

	var meteoResp OpenMeteoResponse
	if err := json.Unmarshal(body, &meteoResp); err != nil {
		return nil, fmt.Errorf("failed to parse weather data: %v", err)
	}

	weatherData := &WeatherData{
		Temperature:   meteoResp.Current.Temperature,
		Humidity:      meteoResp.Current.Humidity,
		WindDirection: meteoResp.Current.WindDirection,
		WindSpeed:     meteoResp.Current.WindSpeed,
		Timestamp:     time.Now().Format(time.RFC3339),
	}

	return weatherData, nil
}

// generateWeatherData fetches real weather data from Open-Meteo API
func generateWeatherData() WeatherData {
	city, exists := cities[currentCity]
	if !exists {
		log.Printf("⚠ City %s not found, using default: %s", currentCity, DefaultCity)
		city = cities[DefaultCity]
		currentCity = DefaultCity
	}

	weatherData, err := fetchWeatherFromOpenMeteo(city)
	if err != nil {
		log.Printf("✗ Error fetching weather data: %v", err)
		// Return dummy data on error
		return WeatherData{
			Temperature:   20.0,
			Humidity:      50.0,
			WindDirection: 0.0,
			WindSpeed:     0.0,
			Timestamp:     time.Now().Format(time.RFC3339),
		}
	}

	return *weatherData
}

// MQTT message handler callbacks
var messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
	log.Printf("📨 Received message on topic: %s\n", msg.Topic())
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
	log.Println("✓ Connected to MQTT Broker")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
	log.Printf("⚠ Connection lost: %v\n", err)
}

// publishWeatherData publishes weather data to MQTT broker
func publishWeatherData(client mqtt.Client, data WeatherData) error {
	payload, err := json.Marshal(data)
	if err != nil {
		return fmt.Errorf("failed to marshal weather data: %v", err)
	}

	token := client.Publish(MQTTTopic, 0, false, payload)
	token.Wait()

	if token.Error() != nil {
		return fmt.Errorf("failed to publish message: %v", token.Error())
	}

	log.Printf("📡 Published [%s]: Temp=%.2f°C, Humidity=%.2f%%, Wind=%.2fkm/h @ %.2f°",
		currentCity, data.Temperature, data.Humidity, data.WindSpeed, data.WindDirection)

	return nil
}

// setupMQTTClient creates and configures an MQTT client
func setupMQTTClient() mqtt.Client {
	opts := mqtt.NewClientOptions()
	opts.AddBroker(MQTTBroker)
	opts.SetClientID(ClientID)
	opts.SetDefaultPublishHandler(messagePubHandler)
	opts.OnConnect = connectHandler
	opts.OnConnectionLost = connectLostHandler
	opts.SetAutoReconnect(true)
	opts.SetConnectRetry(true)
	opts.SetConnectRetryInterval(5 * time.Second)

	client := mqtt.NewClient(opts)
	return client
}

func main() {
	fmt.Println("============================================================")
	fmt.Println("🌤️  Weather Dashboard - Real Weather Data Provider")
	fmt.Println("============================================================")
	fmt.Printf("📡 MQTT Broker: %s\n", MQTTBroker)
	fmt.Printf("📋 MQTT Topic: %s\n", MQTTTopic)
	fmt.Printf("⏱️  Publish Interval: %v\n", PublishInterval)
	fmt.Printf("🌍 Default City: %s\n", currentCity)
	fmt.Println("============================================================")

	// Setup MQTT client
	client := setupMQTTClient()

	// Connect to MQTT broker
	log.Println("🔄 Connecting to MQTT broker...")
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		log.Fatalf("✗ Failed to connect to MQTT broker: %v", token.Error())
	}

	// Setup graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

	// Start publishing weather data
	ticker := time.NewTicker(PublishInterval)
	defer ticker.Stop()

	log.Println("✓ Starting weather data fetching from Open-Meteo API...")

	// Fetch and publish initial data immediately
	weatherData := generateWeatherData()
	if err := publishWeatherData(client, weatherData); err != nil {
		log.Printf("✗ Error publishing data: %v", err)
	}

	for {
		select {
		case <-ticker.C:
			// Generate and publish weather data
			weatherData := generateWeatherData()
			if err := publishWeatherData(client, weatherData); err != nil {
				log.Printf("✗ Error publishing data: %v", err)
			}

		case <-sigChan:
			// Graceful shutdown
			fmt.Println("\n\n🛑 Shutting down gracefully...")
			client.Disconnect(250)
			log.Println("✓ Disconnected from MQTT broker")
			log.Println("👋 Goodbye!")
			return
		}
	}
}
