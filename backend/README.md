# XiaoYue - Wuxia Chinese Learning Chatbot Backend

A Django Channels-based WebSocket backend for an AI-powered Chinese language learning chatbot with a unique Wuxia martial arts theme.

## 🎭 Features

- **Real-time WebSocket Communication**: Instant chat responses via Django Channels
- **AI-Powered Tutoring**: Google Gemini 2.0 Flash with structured output
- **Text-to-Speech**: Edge-TTS for natural Chinese pronunciation
- **Stateful Conversations**: Redis-backed conversation history and user state
- **Emotional Intelligence**: "Sulking level" system for dynamic character personality
- **Wuxia Roleplay**: Unique martial arts themed learning experience

## 🏗️ Architecture

```
Backend Stack:
├── Django 5.x (ASGI mode)
├── Django Channels (WebSocket)
├── PostgreSQL (Database)
├── Redis (Cache & Channel Layer)
├── Google Gemini 2.0 Flash (AI)
└── Edge-TTS (Text-to-Speech)
```

## 📁 Project Structure

```
backend/
├── apps/
│   └── xiaoyue/
│       ├── services/
│       │   ├── ai_agent.py          # Gemini AI integration
│       │   ├── tts_handler.py       # Edge-TTS audio generation
│       │   ├── redis_client.py      # Redis operations
│       │   └── prompts.py           # System prompts & config
│       ├── consumers.py             # WebSocket consumer
│       ├── routing.py               # WebSocket URL routing
│       ├── models.py                # Django models
│       └── tests/                   # Unit tests
├── config/
│   ├── settings.py                  # Django settings
│   ├── asgi.py                      # ASGI configuration
│   └── urls.py                      # HTTP URL routing
├── requirements.txt
├── pytest.ini
└── .env.example
```

## 🚀 Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Redis 6+
- Google Gemini API Key

### Setup Steps

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Redis** (if not running)
   ```bash
   redis-server
   ```

8. **Start development server**
   ```bash
   # Using Daphne (recommended for Channels)
   daphne -b 127.0.0.1 -p 8000 config.asgi:application
   
   # Or using Django runserver (limited WebSocket support)
   python manage.py runserver
   ```

## 🔌 WebSocket API

### Connection

Connect to the WebSocket endpoint:

```javascript
ws://localhost:8000/ws/chat/<user_id>/
// or
ws://localhost:8000/ws/chat/
```

### Message Format

**Client → Server:**

```json
{
  "action": "chat",
  "message": "你好，小师妹",
  "user_role": "师兄"
}
```

**Server → Client:**

```json
{
  "status": "success",
  "data": {
    "thought": "User greeted me, I should respond warmly",
    "chinese_content": "师兄好~！很高兴见到你！",
    "vietnamese_display": "Chào sư huynh! Rất vui được gặp anh!",
    "pinyin": "Shī xiōng hǎo~! Hěn gāoxìng jiàn dào nǐ!",
    "emotion": "happy",
    "action": "none",
    "quiz_list": [],
    "audio_base64": "SUQzBAAAAAAAI1RTU0UAAAA...",
    "sulking_level": 0,
    "timestamp": "2025-12-25T10:00:00Z"
  }
}
```

### Actions

| Action | Description | Parameters |
|--------|-------------|------------|
| `chat` | Send chat message | `message`, `user_role` (optional) |
| `reset` | Clear conversation history | None |
| `get_state` | Get current user state | None |
| `set_sulking` | Set sulking level (testing) | `level` (0-3) |

### Emotions

- `neutral` - Normal teaching mode
- `happy` - Cheerful and encouraging
- `excited` - Very enthusiastic
- `strict` - Serious teaching mode
- `sulking` - Slightly upset (Level 1-2)
- `angry` - Very upset (Level 3)
- `shy` - Bashful response
- `proud` - Satisfied with student progress
- `teasing` - Playful interaction
- `concerned` - Worried about student

### Sulking Level System

The AI character has a "sulking level" (0-3) that affects personality:

- **Level 0**: Happy and helpful
- **Level 1**: Slightly pouty but still teaches
- **Level 2**: Noticeably upset, responses have attitude
- **Level 3**: Refuses to teach unless apologized to

## 🧪 Testing

Run unit tests:

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-django

# Run all tests
pytest

# Run specific test file
pytest apps/xiaoyue/tests/test_ai_agent.py

# Run with coverage
pytest --cov=apps.xiaoyue
```

## 🔧 Configuration

### Redis Keys

- `chat:history:{user_id}` - Conversation history
- `chat:state:{user_id}` - User state (role, preferences)
- `chat:sulking:{user_id}` - Current sulking level

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Gemini API key | Required |
| `POSTGRES_DB` | Database name | `xiaoyue_db` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | Required |
| `POSTGRES_HOST` | Database host | `127.0.0.1` |
| `REDIS_HOST` | Redis host | `127.0.0.1` |

### TTS Voices

Available Chinese voices (Edge-TTS):

- `zh-CN-XiaoxiaoNeural` - Young female (default)
- `zh-CN-YunxiNeural` - Male
- `zh-CN-XiaoyiNeural` - Female
- `zh-CN-YunjianNeural` - Male

## 📊 Performance Tips

1. **Redis Connection Pooling**: Already configured in settings
2. **Async Operations**: All I/O operations use `async/await`
3. **History Limiting**: Conversations limited to last 20 turns
4. **TTS Caching**: Consider caching common phrases (future enhancement)
5. **Rate Limiting**: Add rate limiting for production (recommended)

## 🐛 Debugging

### Enable debug logging

In `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### Check WebSocket connection

```python
# In browser console
const ws = new WebSocket('ws://localhost:8000/ws/chat/test_user/');
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Message:', JSON.parse(e.data));
ws.send(JSON.stringify({action: 'chat', message: '你好'}));
```

## 🔐 Security Considerations

**Production Checklist:**

- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS/WSS in production
- [ ] Add authentication middleware
- [ ] Implement rate limiting
- [ ] Sanitize user inputs (already basic implementation)
- [ ] Use environment variables for secrets
- [ ] Configure CORS properly
- [ ] Add CSRF protection where needed

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines]

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Contact: [your contact info]

---

Made with ❤️ for Chinese language learners

