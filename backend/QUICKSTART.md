# Quick Start Guide - XiaoYue Backend

Get your Chinese learning chatbot running in 10 minutes! ⚡

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.10 or higher
- ✅ PostgreSQL running
- ✅ Redis running
- ✅ Google Gemini API key

## Quick Setup (5 steps)

### 1️⃣ Install Dependencies

```bash
# Windows PowerShell
.\setup.ps1

# Linux/Mac
bash setup.sh
```

Or manually:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2️⃣ Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GOOGLE_API_KEY=your-gemini-api-key-here
POSTGRES_PASSWORD=your-postgres-password
```

### 3️⃣ Run Database Migrations

```bash
python manage.py migrate
```

### 4️⃣ Test Services

```bash
# Test Redis connection
python manage.py test_redis

# Test Gemini API
python manage.py test_gemini

# Test TTS
python manage.py test_tts
```

### 5️⃣ Start Server

```bash
daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

Server will start at: `http://127.0.0.1:8000`

WebSocket endpoint: `ws://127.0.0.1:8000/ws/chat/`

## Test WebSocket Connection

### Option 1: Use Test Client

```bash
python test_websocket_client.py
```

### Option 2: Browser Console

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/test_user/');

ws.onopen = () => {
    console.log('Connected!');
    ws.send(JSON.stringify({
        action: 'chat',
        message: '你好，小师妹',
        user_role: '师兄'
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Response:', data);
};
```

### Option 3: Use Postman/Insomnia

1. Create new WebSocket request
2. URL: `ws://localhost:8000/ws/chat/`
3. Send:
   ```json
   {
       "action": "chat",
       "message": "你好",
       "user_role": "师兄"
   }
   ```

## Expected Response

```json
{
    "status": "success",
    "data": {
        "thought": "User greeted me...",
        "chinese_content": "师兄好~！很高兴见到你！",
        "vietnamese_display": "Chào sư huynh!...",
        "pinyin": "Shī xiōng hǎo~!...",
        "emotion": "happy",
        "action": "none",
        "quiz_list": [],
        "audio_base64": "SUQzBAAAAAAAI1RTU0UAAAA...",
        "sulking_level": 0,
        "timestamp": "2025-12-25T10:00:00Z"
    }
}
```

## Common Commands

```bash
# Run tests
pytest

# Run specific test
pytest apps/xiaoyue/tests/test_ai_agent.py

# Create superuser
python manage.py createsuperuser

# Access admin panel
# http://127.0.0.1:8000/admin/

# Reset conversation history (Redis)
redis-cli
> KEYS chat:*
> DEL chat:history:user_id
> exit

# View logs
# (Logs will appear in console where Daphne is running)
```

## Troubleshooting

### "Connection refused"
- ✅ Check if Redis is running: `redis-cli ping`
- ✅ Check if PostgreSQL is running
- ✅ Check if port 8000 is available

### "Invalid API key"
- ✅ Verify GOOGLE_API_KEY in `.env`
- ✅ Check API key permissions at Google AI Studio

### "WebSocket connection failed"
- ✅ Use Daphne, not Django runserver
- ✅ Check firewall settings
- ✅ Verify WebSocket URL (ws:// not http://)

### "Import Error"
- ✅ Activate virtual environment
- ✅ Run `pip install -r requirements.txt`

## API Reference

### Actions

| Action | Description | Example |
|--------|-------------|---------|
| `chat` | Send message | `{"action": "chat", "message": "你好"}` |
| `reset` | Clear history | `{"action": "reset"}` |
| `get_state` | Get user state | `{"action": "get_state"}` |
| `set_sulking` | Set sulking level | `{"action": "set_sulking", "level": 2}` |

### User Roles

- `师兄` (Shī xiōng) - Senior Brother (default)
- `师姐` (Shī jiě) - Senior Sister
- `师弟` (Shī dì) - Junior Brother
- `师妹` (Shī mèi) - Junior Sister

### Sulking Levels

- **0** = Happy and helpful
- **1** = Slightly pouty
- **2** = Noticeably upset
- **3** = Refuses to teach

## Development Tips

### Hot Reload
Daphne doesn't support hot reload. Use watchdog:

```bash
pip install watchdog
watchmedo auto-restart --pattern="*.py" --recursive -- daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

### Debug Mode
Set `DEBUG=True` in `.env` for detailed error messages.

### Database GUI
Use pgAdmin or DBeaver to inspect PostgreSQL data.

### Redis GUI
Use Redis Commander:
```bash
npm install -g redis-commander
redis-commander
```

## Next Steps

✅ Backend is running!

Now you can:
1. Build a frontend client (React, Vue, etc.)
2. Customize the system prompts in `services/prompts.py`
3. Add more emotions and actions
4. Implement user authentication
5. Add quiz generation logic
6. Deploy to production (see DEPLOYMENT.md)

## Need Help?

- 📖 Read the full README.md
- 🚀 Check DEPLOYMENT.md for production setup
- 🧪 Review test files in `apps/xiaoyue/tests/`
- 🔍 Check Django logs and Redis logs

---

Happy coding! 祝你成功！(Zhù nǐ chénggōng!)

