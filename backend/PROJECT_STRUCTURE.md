# XiaoYue Backend - Project Structure

Complete overview of all components and their purposes.

## 📁 Directory Structure

```
backend/
├── apps/
│   └── xiaoyue/                      # Main application
│       ├── services/                 # Service layer (AI, TTS, Redis)
│       │   ├── __init__.py          # Package exports
│       │   ├── ai_agent.py          # ⭐ Gemini AI integration
│       │   ├── tts_handler.py       # ⭐ Edge-TTS audio generation
│       │   ├── redis_client.py      # ⭐ Redis operations
│       │   └── prompts.py           # System prompts & config
│       ├── management/               # Django management commands
│       │   └── commands/
│       │       ├── test_gemini.py   # Test Gemini API
│       │       ├── test_redis.py    # Test Redis connection
│       │       └── test_tts.py      # Test TTS functionality
│       ├── tests/                    # Unit tests
│       │   ├── test_ai_agent.py
│       │   ├── test_tts_handler.py
│       │   └── test_redis_client.py
│       ├── consumers.py              # ⭐ WebSocket consumer
│       ├── routing.py                # WebSocket URL routing
│       ├── models.py                 # Database models
│       ├── admin.py                  # Django admin config
│       ├── views.py                  # HTTP views
│       ├── urls.py                   # HTTP URL routing
│       └── utils.py                  # Utility functions
├── config/
│   ├── settings.py                   # Django settings
│   ├── asgi.py                       # ⭐ ASGI configuration
│   ├── urls.py                       # Main URL routing
│   └── celery.py                     # Celery configuration
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Pytest configuration
├── .env.example                       # Environment variables template
├── manage.py                          # Django management script
├── test_websocket_client.py          # WebSocket test client
├── setup.sh                           # Linux/Mac setup script
├── setup.ps1                          # Windows setup script
├── README.md                          # Main documentation
├── QUICKSTART.md                      # Quick start guide
├── DEPLOYMENT.md                      # Deployment guide
└── PROJECT_STRUCTURE.md               # This file
```

⭐ = Core files you need to understand

## 🔑 Core Components

### 1. AI Service Layer (`services/ai_agent.py`)

**Purpose**: Interface with Google Gemini 2.0 Flash API

**Key Features**:
- Structured output with JSON schema
- Conversation history management
- Emotion-based responses
- Fallback responses on API failure
- Async/await for non-blocking calls

**Main Class**: `ChineseTutorAgent`

**Key Method**:
```python
async def generate_response(
    user_text: str,
    user_role: str,
    agent_role: str,
    sulking_level: int,
    conversation_history: List[Dict]
) -> Dict[str, Any]
```

**Response Schema**:
```json
{
    "thought": "string",
    "chinese_content": "string",
    "vietnamese_display": "string",
    "pinyin": "string",
    "emotion": "enum[happy, sulking, ...]",
    "action": "enum[none, correction, quiz, ...]",
    "quiz_list": [{"question": "...", "options": [...], "correct_answer": "..."}]
}
```

---

### 2. TTS Handler (`services/tts_handler.py`)

**Purpose**: Convert Chinese text to speech using Edge-TTS

**Key Features**:
- In-memory audio generation (no disk writes)
- Base64 encoding for WebSocket transmission
- Emotion-based voice modulation
- Multiple voice support
- Async streaming

**Main Functions**:
```python
async def generate_tts_audio(
    text: str,
    voice: str = "zh-CN-XiaoxiaoNeural",
    rate: str = "+0%",
    volume: str = "+0%"
) -> Optional[str]

async def generate_tts_with_emotion(
    text: str,
    emotion: str = "neutral",
    custom_voice: Optional[str] = None
) -> Optional[str]
```

**Voice Presets**:
- `happy`: +5% rate, +5% volume
- `excited`: +10% rate, +10% volume
- `sulking`: -5% rate, -5% volume
- `angry`: normal rate, +10% volume
- `shy`: -10% rate, -10% volume

---

### 3. Redis Client (`services/redis_client.py`)

**Purpose**: Manage conversation history and user state

**Key Features**:
- Async Redis operations
- Conversation history (FIFO list)
- User state management
- Sulking level tracking
- Automatic key expiration

**Main Class**: `RedisClient`

**Key Methods**:
```python
async def get_conversation_history(user_id: str, limit: int = 20)
async def add_to_conversation_history(user_id: str, message: Dict)
async def get_sulking_level(user_id: str) -> int
async def set_sulking_level(user_id: str, level: int)
async def get_user_state(user_id: str) -> Dict
async def set_user_state(user_id: str, state: Dict)
```

**Redis Key Patterns**:
- `chat:history:{user_id}` - Conversation history (List)
- `chat:state:{user_id}` - User state (String/JSON)
- `chat:sulking:{user_id}` - Sulking level (Integer 0-3)

---

### 4. WebSocket Consumer (`consumers.py`)

**Purpose**: Handle real-time chat via WebSocket

**Key Features**:
- Async message handling
- Connection lifecycle management
- Multiple action types
- Error handling with graceful fallbacks
- Typing indicators

**Main Class**: `ChineseTutorConsumer(AsyncWebsocketConsumer)`

**Lifecycle**:
```
connect() → accept() → load user state → send welcome
    ↓
receive() → route action → handle_*() → process → send response
    ↓
disconnect() → close Redis connection
```

**Actions Supported**:
- `chat` - Main conversation
- `reset` - Clear history
- `get_state` - Get user state
- `set_sulking` - Set sulking level (testing)

**Message Flow**:
```
Client → {"action": "chat", "message": "你好"}
    ↓
Server: Load history from Redis
    ↓
Server: Call AI agent
    ↓
Server: Generate TTS
    ↓
Server: Save to Redis
    ↓
Server → {"status": "success", "data": {...}}
```

---

### 5. System Prompts (`services/prompts.py`)

**Purpose**: Configure AI personality and behavior

**Key Components**:
- `SYSTEM_PROMPT_TEMPLATE` - Main instruction template
- `EMOTION_OPTIONS` - Available emotions
- `ACTION_OPTIONS` - Available action types
- `REDIS_KEY_PATTERNS` - Redis key naming

**Template Variables**:
- `{agent_role}` - AI character role (小师妹)
- `{user_role}` - User role (师兄/师姐)
- `{sulking_level}` - Current mood (0-3)

---

### 6. ASGI Configuration (`config/asgi.py`)

**Purpose**: Configure Django Channels for WebSocket support

**Protocol Router**:
```python
ProtocolTypeRouter({
    "http": django_asgi_app,           # HTTP requests
    "websocket": AuthMiddlewareStack(  # WebSocket requests
        URLRouter(websocket_urlpatterns)
    ),
})
```

---

## 🔄 Request Flow Diagram

```
WebSocket Client (Browser/App)
    ↓
ws://localhost:8000/ws/chat/user_123/
    ↓
Django Channels (ASGI)
    ↓
ChineseTutorConsumer.receive()
    ↓
┌──────────────────────────────────────┐
│ 1. Load user state from Redis        │
│ 2. Get conversation history          │
│ 3. Extract sulking level             │
└──────────────────────────────────────┘
    ↓
ChineseTutorAgent.generate_response()
    ↓
┌──────────────────────────────────────┐
│ 1. Format system prompt              │
│ 2. Call Gemini API                   │
│ 3. Parse structured JSON response    │
└──────────────────────────────────────┘
    ↓
generate_tts_with_emotion()
    ↓
┌──────────────────────────────────────┐
│ 1. Call Edge-TTS API                 │
│ 2. Stream audio chunks               │
│ 3. Convert to Base64                 │
└──────────────────────────────────────┘
    ↓
Save to Redis
    ↓
┌──────────────────────────────────────┐
│ 1. Add user message to history       │
│ 2. Add AI response to history        │
│ 3. Update user state if needed       │
└──────────────────────────────────────┘
    ↓
Send response to client
    ↓
Client receives JSON with audio
```

---

## 📊 Data Flow

### Conversation History Format
```json
[
    {
        "role": "user",
        "content": "你好，小师妹",
        "timestamp": "2025-12-25T10:00:00Z"
    },
    {
        "role": "assistant",
        "content": "师兄好~！",
        "emotion": "happy",
        "timestamp": "2025-12-25T10:00:01Z"
    }
]
```

### User State Format
```json
{
    "user_role": "师兄",
    "agent_role": "小师妹",
    "sulking_level": 0,
    "preferred_voice": "zh-CN-XiaoxiaoNeural"
}
```

---

## 🧪 Testing

### Unit Tests
- `test_ai_agent.py` - AI service tests
- `test_tts_handler.py` - TTS tests
- `test_redis_client.py` - Redis operations tests

### Integration Tests
- `test_websocket_client.py` - WebSocket client

### Management Commands
- `python manage.py test_gemini` - Test Gemini API
- `python manage.py test_redis` - Test Redis
- `python manage.py test_tts` - Test TTS

---

## 🔧 Configuration Files

### `.env` (Environment Variables)
```env
SECRET_KEY=...
DEBUG=True
GOOGLE_API_KEY=...
POSTGRES_DB=xiaoyue_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=...
```

### `settings.py` (Django Settings)
- Database: PostgreSQL
- Cache: Redis via Channels
- ASGI application
- CORS configuration
- Celery configuration (optional)

### `requirements.txt` (Dependencies)
- Django 5.x
- Channels with Daphne
- Google GenAI SDK
- Edge-TTS
- Redis client
- PostgreSQL adapter
- Testing libraries

---

## 🚀 Deployment Considerations

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS/WSS
- [ ] Set up Nginx reverse proxy
- [ ] Configure Redis authentication
- [ ] Use PostgreSQL SSL
- [ ] Implement rate limiting
- [ ] Set up monitoring (Sentry)
- [ ] Configure backups
- [ ] Use systemd service

### Performance Tips
- Redis connection pooling (built-in)
- Async I/O operations (implemented)
- History limiting (20 turns max)
- Consider TTS caching for common phrases
- Use CDN for static files in production

---

## 📝 Customization Guide

### Change AI Personality
Edit `services/prompts.py`:
- Modify `SYSTEM_PROMPT_TEMPLATE`
- Add new emotions to `EMOTION_OPTIONS`
- Add new actions to `ACTION_OPTIONS`

### Add New Voices
Edit `services/tts_handler.py`:
- Add entries to `VOICE_PRESETS`
- Use different Edge-TTS voices

### Add New Actions
1. Add action to `services/prompts.py`
2. Update Gemini schema in `services/ai_agent.py`
3. Add handler in `consumers.py`

### Custom User Roles
Edit `services/prompts.py`:
- Update system prompt to support new roles
- Adjust wording based on role relationships

---

## 🤝 Contributing

When adding new features:
1. Follow async/await patterns
2. Add type hints (Python 3.10+)
3. Write unit tests
4. Update documentation
5. Check linter (no errors)

---

## 📚 Additional Resources

- [Django Channels Docs](https://channels.readthedocs.io/)
- [Google Gemini API](https://ai.google.dev/)
- [Edge-TTS GitHub](https://github.com/rany2/edge-tts)
- [Redis Commands](https://redis.io/commands/)

---

**Last Updated**: December 25, 2025
**Version**: 1.0.0

