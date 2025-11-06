#!/bin/bash

# Weather Dashboard - Quick Start Script
# This script helps start all components of the Weather Dashboard

echo "============================================================"
echo "🌤️  Weather Dashboard - Quick Start"
echo "============================================================"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Mosquitto is running
check_mosquitto() {
    echo -e "\n${YELLOW}Checking MQTT Broker (Mosquitto)...${NC}"
    if pgrep -x "mosquitto" > /dev/null; then
        echo -e "${GREEN}✓ Mosquitto is running${NC}"
        return 0
    else
        echo -e "${RED}✗ Mosquitto is not running${NC}"
        echo "Please start Mosquitto:"
        echo "  macOS: brew services start mosquitto"
        echo "  Linux: sudo systemctl start mosquitto"
        echo "  Manual: mosquitto -v"
        return 1
    fi
}

# Check Python dependencies
check_python() {
    echo -e "\n${YELLOW}Checking Python dependencies...${NC}"
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
    fi

    source venv/bin/activate

    if pip show Flask > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Python dependencies installed${NC}"
        return 0
    else
        echo -e "${YELLOW}Installing Python dependencies...${NC}"
        pip install -r requirements.txt
        return 0
    fi
}

# Check Go dependencies
check_go() {
    echo -e "\n${YELLOW}Checking Go dependencies...${NC}"
    if [ -f "go.mod" ]; then
        go mod download
        echo -e "${GREEN}✓ Go dependencies ready${NC}"
        return 0
    else
        echo -e "${RED}✗ go.mod not found${NC}"
        return 1
    fi
}

# Main menu
show_menu() {
    echo -e "\n${YELLOW}What would you like to do?${NC}"
    echo "1) Start Python Flask Backend only"
    echo "2) Start Golang Mock Server only"
    echo "3) Start both (recommended)"
    echo "4) Run system checks only"
    echo "5) Exit"
    echo -n "Enter choice [1-5]: "
}

start_python() {
    echo -e "\n${GREEN}Starting Python Flask Backend...${NC}"
    source venv/bin/activate
    python app.py
}

start_golang() {
    echo -e "\n${GREEN}Starting Golang Mock Server...${NC}"
    go run main.go
}

start_both() {
    echo -e "\n${GREEN}Starting both services...${NC}"
    echo "Opening new terminal windows..."

    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && python app.py"'
        sleep 2
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && go run main.go"'
        echo -e "${GREEN}✓ Services started in separate terminal windows${NC}"
    # Linux with gnome-terminal
    elif command -v gnome-terminal > /dev/null; then
        gnome-terminal -- bash -c "cd $(pwd) && source venv/bin/activate && python app.py; exec bash"
        sleep 2
        gnome-terminal -- bash -c "cd $(pwd) && go run main.go; exec bash"
        echo -e "${GREEN}✓ Services started in separate terminal windows${NC}"
    else
        echo -e "${YELLOW}⚠ Cannot open new terminals automatically${NC}"
        echo "Please run these commands in separate terminals:"
        echo ""
        echo "Terminal 1: source venv/bin/activate && python app.py"
        echo "Terminal 2: go run main.go"
    fi
}

# Main execution
main() {
    # Run checks
    if ! check_mosquitto; then
        exit 1
    fi

    check_python
    check_go

    # Show menu and handle choice
    while true; do
        show_menu
        read choice

        case $choice in
            1)
                start_python
                break
                ;;
            2)
                start_golang
                break
                ;;
            3)
                start_both
                echo -e "\n${GREEN}✓ Check the new terminal windows${NC}"
                echo "Press Ctrl+C in each window to stop services"
                exit 0
                ;;
            4)
                echo -e "\n${GREEN}✓ All checks completed${NC}"
                exit 0
                ;;
            5)
                echo -e "\n${GREEN}Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${NC}"
                ;;
        esac
    done
}

# Run main function
main
