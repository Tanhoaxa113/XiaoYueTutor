# Deployment Guide for XiaoYue Backend

This guide covers deploying the XiaoYue Chinese Learning Chatbot backend to production.

## 🌐 Deployment Options

### Option 1: Traditional VPS (Ubuntu/Debian)

#### Prerequisites
- Ubuntu 20.04+ or Debian 11+
- Root or sudo access
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

#### Installation Steps

1. **Update system and install dependencies**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3.10 python3.10-venv python3-pip postgresql postgresql-contrib redis-server nginx git -y
```

2. **Create application user**
```bash
sudo adduser xiaoyue
sudo usermod -aG sudo xiaoyue
su - xiaoyue
```

3. **Clone repository**
```bash
cd /opt
sudo git clone <your-repo-url> xiaoyue
sudo chown -R xiaoyue:xiaoyue /opt/xiaoyue
cd /opt/xiaoyue/backend
```

4. **Setup virtual environment**
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn uvicorn[standard]
```

5. **Configure PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE xiaoyue_db;
CREATE USER xiaoyue_user WITH PASSWORD 'your_secure_password';
ALTER ROLE xiaoyue_user SET client_encoding TO 'utf8';
ALTER ROLE xiaoyue_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE xiaoyue_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE xiaoyue_db TO xiaoyue_user;
\q
```

6. **Configure environment variables**
```bash
cp .env.example .env
nano .env
```

Update `.env`:
```env
SECRET_KEY=your_production_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

GOOGLE_API_KEY=your_gemini_api_key

POSTGRES_DB=xiaoyue_db
POSTGRES_USER=xiaoyue_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_HOST=localhost
```

7. **Run migrations**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

8. **Create systemd service for Daphne (WebSocket)**
```bash
sudo nano /etc/systemd/system/xiaoyue-daphne.service
```

Content:
```ini
[Unit]
Description=XiaoYue Daphne WebSocket Service
After=network.target

[Service]
Type=simple
User=xiaoyue
Group=xiaoyue
WorkingDirectory=/opt/xiaoyue/backend
Environment="PATH=/opt/xiaoyue/backend/venv/bin"
ExecStart=/opt/xiaoyue/backend/venv/bin/daphne -b 127.0.0.1 -p 8000 config.asgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

9. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/xiaoyue
```

Content:
```nginx
upstream daphne {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Static files
    location /static/ {
        alias /opt/xiaoyue/backend/staticfiles/;
        expires 30d;
    }
    
    # WebSocket
    location /ws/ {
        proxy_pass http://daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
    
    # HTTP requests
    location / {
        proxy_pass http://daphne;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/xiaoyue /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

10. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

11. **Start services**
```bash
sudo systemctl start xiaoyue-daphne
sudo systemctl enable xiaoyue-daphne
sudo systemctl status xiaoyue-daphne
```

---

### Option 2: Docker Deployment

#### Create Dockerfile
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations and start server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
```

#### Create docker-compose.yml
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: xiaoyue_db
      POSTGRES_USER: xiaoyue
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - xiaoyue_network

  redis:
    image: redis:7-alpine
    networks:
      - xiaoyue_network

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - POSTGRES_HOST=postgres
      - POSTGRES_DB=xiaoyue_db
      - POSTGRES_USER=xiaoyue
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - redis
    networks:
      - xiaoyue_network

volumes:
  postgres_data:

networks:
  xiaoyue_network:
```

Run with:
```bash
docker-compose up -d
```

---

### Option 3: Cloud Platforms

#### Railway.app
1. Connect GitHub repository
2. Add PostgreSQL and Redis plugins
3. Set environment variables
4. Deploy automatically

#### Heroku
```bash
heroku create xiaoyue-backend
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
heroku config:set GOOGLE_API_KEY=your_key
git push heroku main
```

#### AWS Elastic Beanstalk
1. Install EB CLI
2. Configure `eb init`
3. Create environment with RDS and ElastiCache
4. Deploy with `eb deploy`

---

## 🔒 Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use HTTPS/WSS (SSL certificates)
- [ ] Set up firewall (UFW/iptables)
- [ ] Enable Redis password authentication
- [ ] Use PostgreSQL SSL connections
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Set up monitoring (Sentry, CloudWatch, etc.)
- [ ] Regular backups of database
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets

---

## 📊 Monitoring

### Add Sentry for error tracking
```bash
pip install sentry-sdk
```

In `settings.py`:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

### System monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop netstat-nat

# Check logs
sudo journalctl -u xiaoyue-daphne -f
```

---

## 🔧 Maintenance

### Database backups
```bash
# Backup
pg_dump xiaoyue_db > backup_$(date +%Y%m%d).sql

# Restore
psql xiaoyue_db < backup_20251225.sql
```

### Update application
```bash
cd /opt/xiaoyue/backend
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
sudo systemctl restart xiaoyue-daphne
```

---

## 🚨 Troubleshooting

### WebSocket connection fails
- Check firewall rules
- Verify Nginx WebSocket configuration
- Check Daphne service status
- Review logs: `journalctl -u xiaoyue-daphne`

### Redis connection issues
- Verify Redis is running: `redis-cli ping`
- Check Redis configuration
- Ensure correct Redis URL in settings

### Database connection errors
- Check PostgreSQL status: `sudo systemctl status postgresql`
- Verify credentials in `.env`
- Check PostgreSQL logs

---

## 📞 Support

For deployment issues, check:
- Application logs
- Nginx error logs: `/var/log/nginx/error.log`
- System logs: `journalctl -xe`
- Redis logs: `/var/log/redis/redis-server.log`

