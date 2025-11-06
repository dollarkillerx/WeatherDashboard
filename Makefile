.PHONY: help install install-python install-go run-python run-go test clean check-mosquitto

# Default target
help:
	@echo "Weather Dashboard - Makefile Commands"
	@echo "======================================"
	@echo "make install          - Install all dependencies"
	@echo "make install-python   - Install Python dependencies"
	@echo "make install-go       - Install Go dependencies"
	@echo "make run-python       - Run Python Flask backend"
	@echo "make run-go           - Run Golang mock server"
	@echo "make test             - Test API endpoints"
	@echo "make check-mosquitto  - Check if MQTT broker is running"
	@echo "make clean            - Clean build artifacts and cache"

# Install all dependencies
install: install-python install-go
	@echo "✓ All dependencies installed"

# Install Python dependencies
install-python:
	@echo "Installing Python dependencies..."
	@python3 -m venv venv 2>/dev/null || true
	@. venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Python dependencies installed"

# Install Go dependencies
install-go:
	@echo "Installing Go dependencies..."
	@go mod download
	@go mod tidy
	@echo "✓ Go dependencies installed"

# Check if Mosquitto is running
check-mosquitto:
	@echo "Checking MQTT broker..."
	@if pgrep -x mosquitto > /dev/null; then \
		echo "✓ Mosquitto is running"; \
	else \
		echo "✗ Mosquitto is not running"; \
		echo "Start with: brew services start mosquitto (macOS) or sudo systemctl start mosquitto (Linux)"; \
		exit 1; \
	fi

# Run Python backend
run-python: check-mosquitto
	@echo "Starting Python Flask backend..."
	@. venv/bin/activate && python app.py

# Run Golang mock server
run-go: check-mosquitto
	@echo "Starting Golang mock server..."
	@go run main.go

# Test API endpoints
test:
	@echo "Testing API endpoints..."
	@echo "\n1. Health Check:"
	@curl -s http://localhost:5000/api/health | python3 -m json.tool || echo "Backend not running"
	@echo "\n\n2. Current Weather:"
	@curl -s http://localhost:5000/api/weather/current | python3 -m json.tool || echo "No data available"
	@echo "\n\n3. Statistics:"
	@curl -s http://localhost:5000/api/weather/stats | python3 -m json.tool || echo "No data available"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf venv
	@rm -rf __pycache__
	@rm -rf *.pyc
	@go clean
	@echo "✓ Cleaned"
