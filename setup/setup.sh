#!/bin/bash

# Product Opportunity Recommendation System - Setup Script (Linux/macOS)

set -e

echo "========================================"
echo "Product Opportunity Recommendation System"
echo "Quick Setup Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    print_error "Python is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

print_status "Using Python command: $PYTHON_CMD"

# Step 1: Install Node.js dependencies
print_status "[1/5] Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    print_error "npm install failed"
    exit 1
fi

# Step 2: Check AWS CLI configuration
print_status "[2/5] Checking AWS CLI configuration..."
if ! aws sts get-caller-identity &> /dev/null; then
    print_warning "AWS CLI not configured. Run 'aws configure' first."
    read -p "Press Enter to continue anyway..."
fi

# Step 3: Check Bedrock model access
print_status "[3/5] Checking Bedrock model access..."
if [ -f "simple-bedrock-check.py" ]; then
    $PYTHON_CMD simple-bedrock-check.py || print_warning "Bedrock access issue. Check model permissions in AWS Console."
fi

# Step 4: Deploy weather agent
print_status "[4/5] Deploying weather agent..."
cd bedrock-agent
$PYTHON_CMD complete-deploy.py
cd ..

# Step 5: Deploy product opportunity agent
print_status "[5/5] Deploying product opportunity agent..."
cd bedrock-agent/product-opportunity-agent
$PYTHON_CMD simple-deploy.py
cd ../..

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Update src/aws-config.js with your agent IDs"
echo "2. Run 'npm start' to launch the application"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "To verify your setup, run:"
echo "  $PYTHON_CMD verify-setup.py"
echo ""