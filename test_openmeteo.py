#!/usr/bin/env python3
"""Test script to verify Open-Meteo API integration"""

import requests
import json

# City coordinates
CITIES = {
    'Tokyo': {'lat': 35.6895, 'lon': 139.6917},
    'New York': {'lat': 40.7128, 'lon': -74.0060},
}

def test_current_weather(city_name, city_data):
    """Test fetching current weather"""
    print(f"\n{'='*60}")
    print(f"Testing Current Weather for {city_name}")
    print('='*60)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': city_data['lat'],
        'longitude': city_data['lon'],
        'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        print(f"✓ Successfully fetched current weather")
        print(f"Temperature: {data['current']['temperature_2m']}°C")
        print(f"Humidity: {data['current']['relative_humidity_2m']}%")
        print(f"Wind Speed: {data['current']['wind_speed_10m']} km/h")
        print(f"Wind Direction: {data['current']['wind_direction_10m']}°")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_forecast(city_name, city_data):
    """Test fetching 7-day forecast"""
    print(f"\n{'='*60}")
    print(f"Testing 7-Day Forecast for {city_name}")
    print('='*60)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': city_data['lat'],
        'longitude': city_data['lon'],
        'daily': 'temperature_2m_max,temperature_2m_min,relative_humidity_2m_mean,wind_speed_10m_max,wind_direction_10m_dominant',
        'timezone': 'auto'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        print(f"✓ Successfully fetched 7-day forecast")
        daily = data['daily']
        for i in range(min(3, len(daily['time']))):  # Show first 3 days
            print(f"\n{daily['time'][i]}:")
            print(f"  Temp: {daily['temperature_2m_min'][i]}°C - {daily['temperature_2m_max'][i]}°C")
            print(f"  Humidity: {daily['relative_humidity_2m_mean'][i]}%")
            print(f"  Wind: {daily['wind_speed_10m_max'][i]} km/h")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    print("🌤️  Open-Meteo API Integration Test")
    print("="*60)

    results = []

    for city_name, city_data in CITIES.items():
        results.append(test_current_weather(city_name, city_data))
        results.append(test_forecast(city_name, city_data))

    print(f"\n{'='*60}")
    print("Test Summary")
    print('='*60)
    print(f"Total tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")

    if all(results):
        print("\n✓ All tests passed!")
    else:
        print("\n⚠ Some tests failed")
