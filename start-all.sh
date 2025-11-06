#!/bin/bash

# Weather Dashboard - Complete System Start Script
# Starts all three components: Backend, Mock Server, and Frontend

echo "============================================================"
echo "🌤️  Weather Dashboard - Complete System Startup"
echo "============================================================"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Mosquitto is running
check_mosquitto() {
    echo -e "\n${YELLOW}[1/4] Checking MQTT Broker (Mosquitto)...${NC}"
    if pgrep -x "mosquitto" > /dev/null; then
        echo -e "${GREEN}✓ Mosquitto is running${NC}"
        return 0
    else
        echo -e "${RED}✗ Mosquitto is not running${NC}"
        echo "Please start Mosquitto:"
        echo "  macOS: brew services start mosquitto"
        echo "  Linux: sudo systemctl start mosquitto"
        return 1
    fi
}

# Check Python setup
check_python() {
    echo -e "\n${YELLOW}[2/4] Checking Python Backend...${NC}"
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
    fi

    source venv/bin/activate

    if pip show Flask > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Python dependencies installed${NC}"
    else
        echo -e "${YELLOW}Installing Python dependencies...${NC}"
        pip install -r requirements.txt
    fi
    return 0
}

# Check Go setup
check_go() {
    echo -e "\n${YELLOW}[3/4] Checking Golang Mock Server...${NC}"
    if [ -f "go.mod" ]; then
        go mod download > /dev/null 2>&1
        echo -e "${GREEN}✓ Go dependencies ready${NC}"
        return 0
    else
        echo -e "${RED}✗ go.mod not found${NC}"
        return 1
    fi
}

# Check Frontend setup
check_frontend() {
    echo -e "\n${YELLOW}[4/4] Checking Vue Frontend...${NC}"
    if [ ! -d "frontend/node_modules" ]; then
        echo -e "${YELLOW}Installing frontend dependencies...${NC}"
        cd frontend
        pnpm install
        cd ..
    fi
    echo -e "${GREEN}✓ Frontend dependencies ready${NC}"
    return 0
}

# Start all services
start_all() {
    echo -e "\n${GREEN}Starting all services...${NC}"
    echo "Opening terminal windows for each component..."

    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Start Python Backend
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && echo \"🐍 Python Flask Backend\" && python app.py"' > /dev/null 2>&1
        echo -e "${BLUE}Terminal 1:${NC} Python Flask Backend - http://localhost:5000"
        sleep 2

        # Start Golang Server
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && echo \"🔵 Golang Mock Server\" && go run main.go"' > /dev/null 2>&1
        echo -e "${BLUE}Terminal 2:${NC} Golang Mock Server"
        sleep 2

        # Start Frontend
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"'/frontend && echo \"⚡ Vue Frontend\" && pnpm dev"' > /dev/null 2>&1
        echo -e "${BLUE}Terminal 3:${NC} Vue Frontend - http://localhost:3000"

    # Linux with gnome-terminal
    elif command -v gnome-terminal > /dev/null; then
        gnome-terminal --title="Python Backend" -- bash -c "cd $(pwd) && source venv/bin/activate && echo '🐍 Python Flask Backend' && python app.py; exec bash" &
        echo -e "${BLUE}Terminal 1:${NC} Python Flask Backend - http://localhost:5000"
        sleep 2

        gnome-terminal --title="Golang Server" -- bash -c "cd $(pwd) && echo '🔵 Golang Mock Server' && go run main.go; exec bash" &
        echo -e "${BLUE}Terminal 2:${NC} Golang Mock Server"
        sleep 2

        gnome-terminal --title="Vue Frontend" -- bash -c "cd $(pwd)/frontend && echo '⚡ Vue Frontend' && pnpm dev; exec bash" &
        echo -e "${BLUE}Terminal 3:${NC} Vue Frontend - http://localhost:3000"

    else
        echo -e "${YELLOW}⚠ Cannot open terminals automatically${NC}"
        echo ""
        echo "Please run these commands in separate terminals:"
        echo ""
        echo -e "${BLUE}Terminal 1 (Backend):${NC}"
        echo "  source venv/bin/activate && python app.py"
        echo ""
        echo -e "${BLUE}Terminal 2 (Mock Server):${NC}"
        echo "  go run main.go"
        echo ""
        echo -e "${BLUE}Terminal 3 (Frontend):${NC}"
        echo "  cd frontend && pnpm dev"
        return 1
    fi

    return 0
}

# Main execution
main() {
    # Run checks
    if ! check_mosquitto; then
        exit 1
    fi

    check_python
    check_go
    check_frontend

    # Start all services
    if start_all; then
        echo ""
        echo "============================================================"
        echo -e "${GREEN}✓ All services started successfully!${NC}"
        echo "============================================================"
        echo ""
        echo "📍 Access Points:"
        echo -e "   ${BLUE}Frontend Dashboard:${NC} http://localhost:3000"
        echo -e "   ${BLUE}Backend API:${NC}        http://localhost:5000"
        echo ""
        echo "💡 Tips:"
        echo "   - Wait 5-10 seconds for all services to fully start"
        echo "   - Check each terminal window for status"
        echo "   - Press Ctrl+C in each terminal to stop services"
        echo ""
        echo "============================================================"
    fi
}

# Run main function
main
