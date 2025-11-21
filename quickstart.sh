#!/bin/bash
# Quick start script for local development

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
   _____    _             _   _               _                            _             
  /  _  \  | |           | | (_)             | |                          (_)            
 / /_\ \ __| | __ _ _ __ | |_ ___   _____    | |     ___  __ _ _ __ _ __  _ _ __   __ _ 
|  _  |/ _` |/ _` | '_ \| __| \ \ / / _ \   | |    / _ \/ _` | '__| '_ \| | '_ \ / _` |
| | | | (_| | (_| | |_) | |_| |\ V /  __/   | |___|  __/ (_| | |  | | | | | | | | (_| |
\_| |_/\__,_|\__,_| .__/ \__|_| \_/ \___|   \_____/\___|\__,_|_|  |_| |_|_|_| |_|\__, |
                  | |                                                              __/ |
                  |_|                                                             |___/ 
EOF
echo -e "${NC}"

echo -e "${GREEN}=== Adaptive Learning Roadmap - Quick Start ===${NC}\n"

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}Creating .env file from example...${NC}"
    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        echo -e "${GREEN}✓ Created backend/.env${NC}"
        echo -e "${YELLOW}⚠️  Please edit backend/.env and add your configuration!${NC}\n"
    else
        echo -e "${YELLOW}⚠️  backend/.env.example not found. Please create backend/.env manually.${NC}\n"
    fi
fi

# Check if Docker is installed
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo -e "${BLUE}Docker detected! Choose your preferred method:${NC}"
    echo "1. Docker Compose (recommended - runs everything)"
    echo "2. Local development (backend + frontend separately)"
    echo "3. Exit"
    read -p "Enter choice (1-3): " choice
    
    case $choice in
        1)
            echo -e "\n${GREEN}Starting with Docker Compose...${NC}"
            
            # Check if .env file exists for docker-compose
            if [ ! -f ".env" ]; then
                echo -e "${YELLOW}Creating .env file for Docker Compose...${NC}"
                cat > .env << 'ENVFILE'
DATABASE_PASSWORD=changeme
SECRET_KEY=your-secret-key-at-least-32-characters-long-change-this-in-production
GEMINI_API_KEY=
GEMINI_MODEL=gemini-1.5-flash
ENVFILE
                echo -e "${GREEN}✓ Created .env file${NC}"
                echo -e "${YELLOW}⚠️  Please edit .env and set your SECRET_KEY and other values!${NC}\n"
            fi
            
            docker-compose up -d
            echo -e "\n${GREEN}✓ Services started!${NC}"
            echo -e "${BLUE}Access the application at:${NC}"
            echo "  Frontend: http://localhost"
            echo "  Backend API: http://localhost:8000"
            echo "  API Docs: http://localhost:8000/docs"
            echo ""
            echo -e "${YELLOW}View logs:${NC} docker-compose logs -f"
            echo -e "${YELLOW}Stop services:${NC} docker-compose down"
            ;;
        2)
            echo -e "\n${GREEN}Starting local development mode...${NC}\n"
            
            # Check for Python
            if ! command -v python3 &> /dev/null; then
                echo -e "${YELLOW}Python 3 not found. Please install Python 3.11+${NC}"
                exit 1
            fi
            
            # Create virtual environment if it doesn't exist
            if [ ! -d "backend/venv" ]; then
                echo -e "${YELLOW}Creating Python virtual environment...${NC}"
                cd backend
                python3 -m venv venv
                cd ..
                echo -e "${GREEN}✓ Virtual environment created${NC}"
            fi
            
            # Install dependencies
            echo -e "${YELLOW}Installing Python dependencies...${NC}"
            source backend/venv/bin/activate
            pip install -r backend/requirements.txt > /dev/null 2>&1
            echo -e "${GREEN}✓ Dependencies installed${NC}\n"
            
            echo -e "${BLUE}To start the application:${NC}"
            echo ""
            echo "1. Start the backend (in terminal 1):"
            echo "   cd backend"
            echo "   source venv/bin/activate"
            echo "   uvicorn app.main:app --reload"
            echo ""
            echo "2. Serve the frontend (in terminal 2):"
            echo "   cd frontend"
            echo "   python -m http.server 8080"
            echo ""
            echo "3. Access at http://localhost:8080"
            echo ""
            echo -e "${YELLOW}Note: Make sure PostgreSQL is running and configured in backend/.env${NC}"
            ;;
        3)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice"
            exit 1
            ;;
    esac
else
    echo -e "${YELLOW}Docker not detected. Starting in local development mode...${NC}\n"
    
    # Check for Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}Python 3 not found. Please install Python 3.11+${NC}"
        exit 1
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "backend/venv" ]; then
        echo -e "${YELLOW}Creating Python virtual environment...${NC}"
        cd backend
        python3 -m venv venv
        cd ..
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    fi
    
    # Install dependencies
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    source backend/venv/bin/activate
    pip install -r backend/requirements.txt > /dev/null 2>&1
    echo -e "${GREEN}✓ Dependencies installed${NC}\n"
    
    echo -e "${BLUE}To start the application:${NC}"
    echo ""
    echo "1. Start PostgreSQL database"
    echo ""
    echo "2. Start the backend (in terminal 1):"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   uvicorn app.main:app --reload"
    echo ""
    echo "3. Serve the frontend (in terminal 2):"
    echo "   cd frontend"
    echo "   python -m http.server 8080"
    echo ""
    echo "4. Access at http://localhost:8080"
    echo ""
    echo -e "${YELLOW}Note: Make sure PostgreSQL is configured in backend/.env${NC}"
fi
