#!/bin/bash

# XiaoYue Backend Setup Script
# Usage: bash setup.sh

set -e  # Exit on error

echo "=================================="
echo "XiaoYue Backend Setup"
echo "=================================="

# Check Python version
echo ""
echo "📍 Checking Python version..."
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python not found! Please install Python 3.10+"
    exit 1
fi

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo ""
echo "⚡ Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
echo ""
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your API keys!"
    echo ""
else
    echo "✅ .env file exists"
fi

# Check Redis
echo ""
echo "🔍 Checking Redis connection..."
redis-cli ping > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis is not running!"
    echo "   Start Redis with: redis-server"
fi

# Check PostgreSQL
echo ""
echo "🔍 Checking PostgreSQL..."
psql --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ PostgreSQL is installed"
else
    echo "⚠️  PostgreSQL not found!"
fi

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser prompt
echo ""
read -p "Create Django superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Run tests
echo ""
read -p "Run service tests? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Testing Redis..."
    python manage.py test_redis
    
    echo ""
    echo "Testing Gemini API..."
    python manage.py test_gemini
    
    echo ""
    echo "Testing TTS..."
    python manage.py test_tts
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "🚀 To start the server, run:"
echo "   daphne -b 127.0.0.1 -p 8000 config.asgi:application"
echo ""
echo "📝 Don't forget to:"
echo "   1. Configure your .env file with API keys"
echo "   2. Ensure Redis is running"
echo "   3. Ensure PostgreSQL is running"
echo ""

