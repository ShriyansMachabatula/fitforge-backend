#!/bin/bash

# ===========================================
# FitForge Backend Setup Script
# ===========================================
# This script sets up the development environment for new team members

set -e  # Exit on error

echo "==========================================="
echo "🚀 FitForge Backend Setup"
echo "==========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "ℹ️  $1"
}

# Step 1: Check prerequisites
echo "📋 Step 1/6: Checking prerequisites..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker Desktop."
    exit 1
fi

print_success "Docker found"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

print_success "Docker Compose found"

echo ""

# Step 2: Create virtual environment
echo "📦 Step 2/6: Creating virtual environment..."
echo ""

if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

echo ""

# Step 3: Activate virtual environment and install dependencies
echo "📥 Step 3/6: Installing Python dependencies..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip > /dev/null 2>&1

# Install requirements
pip install -r requirements.txt

print_success "Dependencies installed"

echo ""

# Step 4: Set up environment variables
echo "🔧 Step 4/6: Setting up environment variables..."
echo ""

if [ -f ".env" ]; then
    print_warning ".env file already exists. Skipping creation."
    print_info "If you need to reset it, copy from .env.example"
else
    cp .env.example .env
    print_success ".env file created from .env.example"
    print_warning "Please review .env and update if needed (especially for production)"
fi

echo ""

# Step 5: Start PostgreSQL with Docker
echo "🐘 Step 5/6: Starting PostgreSQL database..."
echo ""

# Check if PostgreSQL container is already running
if docker ps | grep -q fitforge-postgres; then
    print_warning "PostgreSQL container already running"
else
    # Start Docker Compose
    docker compose up -d

    # Wait for PostgreSQL to be ready
    print_info "Waiting for PostgreSQL to be ready..."
    sleep 5

    # Check if container is healthy
    if docker ps | grep -q fitforge-postgres; then
        print_success "PostgreSQL started successfully"
    else
        print_error "Failed to start PostgreSQL. Check docker logs."
        exit 1
    fi
fi

echo ""

# Step 6: Initialize database
echo "💾 Step 6/6: Initializing database..."
echo ""

# Create database tables
python -m app.scripts.create_db

print_success "Database initialized"

echo ""
echo "==========================================="
echo "✅ Setup Complete!"
echo "==========================================="
echo ""
echo "🎉 Your FitForge backend is ready to go!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the development server:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3. Visit the API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "4. Test the health endpoint:"
echo "   curl http://localhost:8000/api/health"
echo ""
echo "📚 Useful commands:"
echo ""
echo "  • Run tests:           python test_models.py"
echo "  • Reset database:      python -m app.scripts.create_db --reset --force"
echo "  • Seed database:       python app/seed.py --force"
echo "  • Stop database:       docker compose down"
echo "  • View logs:           docker logs fitforge-postgres"
echo ""
echo "📖 Documentation:"
echo "  • README.md                    - Project overview"
echo "  • VERIFICATION_COMPLETE.md     - Verification guide"
echo "  • DATABASE_MODELS_GUIDE.md     - Database models guide"
echo "  • CONTRIBUTING.md              - Contribution guidelines"
echo ""
echo "Happy coding! 🚀"
echo ""
