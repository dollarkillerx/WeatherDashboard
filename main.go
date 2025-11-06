package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
	"math/rand"
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

// Configuration constants
const (
	MQTTBroker        = "tcp://localhost:1883"
	MQTTTopic         = "weather/data"
	PublishInterval   = 2 * time.Second
	ClientID          = "golang-weather-simulator"
)

// Weather simulation ranges
const (
	TempMin        = 15.0
	TempMax        = 35.0
	HumidityMin    = 30.0
	HumidityMax    = 90.0
	WindSpeedMin   = 0.0
	WindSpeedMax   = 30.0
	WindDirMin     = 0.0
	WindDirMax     = 360.0
)

var (
	currentTemp   float64
	currentHumid  float64
	currentWSpeed float64
	currentWDir   float64
)

// Initialize random values
func init() {
	rand.Seed(time.Now().UnixNano())
	currentTemp = randomInRange(TempMin, TempMax)
	currentHumid = randomInRange(HumidityMin, HumidityMax)
	currentWSpeed = randomInRange(WindSpeedMin, WindSpeedMax)
	currentWDir = randomInRange(WindDirMin, WindDirMax)
}

// randomInRange generates a random float64 between min and max
func randomInRange(min, max float64) float64 {
	return min + rand.Float64()*(max-min)
}

// smoothChange generates a gradual change in value
func smoothChange(current, min, max, maxDelta float64) float64 {
	delta := (rand.Float64() - 0.5) * maxDelta
	newValue := current + delta

	// Keep within bounds
	if newValue < min {
		newValue = min
	}
	if newValue > max {
		newValue = max
	}

	return newValue
}

// generateWeatherData generates realistic weather data with smooth transitions
func generateWeatherData() WeatherData {
	// Generate smooth changes
	currentTemp = smoothChange(currentTemp, TempMin, TempMax, 1.0)
	currentHumid = smoothChange(currentHumid, HumidityMin, HumidityMax, 3.0)
	currentWSpeed = smoothChange(currentWSpeed, WindSpeedMin, WindSpeedMax, 2.0)
	currentWDir = smoothChange(currentWDir, WindDirMin, WindDirMax, 15.0)

	// Round to 2 decimal places
	temperature := math.Round(currentTemp*100) / 100
	humidity := math.Round(currentHumid*100) / 100
	windSpeed := math.Round(currentWSpeed*100) / 100
	windDirection := math.Round(currentWDir*100) / 100

	return WeatherData{
		Temperature:   temperature,
		Humidity:      humidity,
		WindDirection: windDirection,
		WindSpeed:     windSpeed,
		Timestamp:     time.Now().Format(time.RFC3339),
	}
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

	log.Printf("📡 Published: Temp=%.2f°C, Humidity=%.2f%%, Wind=%.2fkm/h @ %.2f°",
		data.Temperature, data.Humidity, data.WindSpeed, data.WindDirection)

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
	fmt.Println("🌤️  Weather Dashboard - Golang MQTT Mock Data Server")
	fmt.Println("============================================================")
	fmt.Printf("📡 MQTT Broker: %s\n", MQTTBroker)
	fmt.Printf("📋 MQTT Topic: %s\n", MQTTTopic)
	fmt.Printf("⏱️  Publish Interval: %v\n", PublishInterval)
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

	log.Println("✓ Starting weather data simulation...")

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
