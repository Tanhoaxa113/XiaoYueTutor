# XiaoYue Backend Setup Script for Windows PowerShell
# Usage: .\setup.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "XiaoYue Backend Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Check Python version
Write-Host "`n📍 Checking Python version..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found! Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`n🔧 Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "`n⚡ Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`n📦 Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if .env exists
Write-Host ""
if (!(Test-Path .env)) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "📝 Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file" -ForegroundColor Green
    Write-Host "⚠️  Please edit .env and add your API keys!" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "✅ .env file exists" -ForegroundColor Green
}

# Check Redis
Write-Host "`n🔍 Checking Redis connection..." -ForegroundColor Yellow
$redisRunning = $false
try {
    $null = redis-cli ping 2>&1
    if ($LASTEXITCODE -eq 0) {
        $redisRunning = $true
    }
} catch {
    $redisRunning = $false
}

if ($redisRunning) {
    Write-Host "✅ Redis is running" -ForegroundColor Green
} else {
    Write-Host "⚠️  Redis is not running!" -ForegroundColor Yellow
    Write-Host "   Start Redis with: redis-server" -ForegroundColor Gray
}

# Check PostgreSQL
Write-Host "`n🔍 Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $null = psql --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ PostgreSQL is installed" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  PostgreSQL not found!" -ForegroundColor Yellow
}

# Run migrations
Write-Host "`n🗄️  Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Create superuser prompt
Write-Host ""
$createSuperuser = Read-Host "Create Django superuser? (y/n)"
if ($createSuperuser -eq "y" -or $createSuperuser -eq "Y") {
    python manage.py createsuperuser
}

# Run tests
Write-Host ""
$runTests = Read-Host "Run service tests? (y/n)"
if ($runTests -eq "y" -or $runTests -eq "Y") {
    Write-Host "`nTesting Redis..." -ForegroundColor Cyan
    python manage.py test_redis
    
    Write-Host "`nTesting Gemini API..." -ForegroundColor Cyan
    python manage.py test_gemini
    
    Write-Host "`nTesting TTS..." -ForegroundColor Cyan
    python manage.py test_tts
}

Write-Host "`n==================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 To start the server, run:" -ForegroundColor Yellow
Write-Host "   daphne -b 127.0.0.1 -p 8000 config.asgi:application" -ForegroundColor White
Write-Host ""
Write-Host "📝 Don't forget to:" -ForegroundColor Yellow
Write-Host "   1. Configure your .env file with API keys" -ForegroundColor Gray
Write-Host "   2. Ensure Redis is running" -ForegroundColor Gray
Write-Host "   3. Ensure PostgreSQL is running" -ForegroundColor Gray
Write-Host ""

