# XiaoYue Frontend - Wuxia Chinese Learning Chat

Beautiful, interactive React frontend for the Chinese learning chatbot with ancient scroll aesthetics.

## 🎨 Features

- **Wuxia Theme**: Ancient Chinese scroll design with parchment colors
- **Real-time Chat**: WebSocket connection to Django backend
- **Audio Playback**: Automatic TTS audio playback with queue management
- **Hanzi Animation**: Interactive character stroke order with hanzi-writer
- **Quiz System**: In-chat interactive quizzes
- **Emotion Display**: Dynamic AI emotion states
- **Responsive Design**: Beautiful on all screen sizes

## 🚀 Quick Start

### Install Dependencies

```bash
npm install
```

### Start Development Server

```bash
npm run dev
```

Frontend will start at: `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## 📁 Project Structure

```
src/
├── components/
│   ├── AgentMessageBubble.jsx    # AI message display with quiz
│   ├── UserMessageBubble.jsx     # User message display
│   ├── ChatHeader.jsx            # Header with status
│   ├── ChatWindow.jsx            # Message list
│   ├── ChatInput.jsx             # Input area
│   ├── HanziPlayer.jsx           # Character animation
│   ├── HanziModal.jsx            # Character modal
│   ├── SettingsModal.jsx         # Settings
│   └── StartOverlay.jsx          # Audio unlock
├── hooks/
│   └── useChat.js                # WebSocket logic
├── store/
│   └── chatStore.js              # Zustand state
├── utils/
│   ├── audioPlayer.js            # Audio utilities
│   └── emotionHelper.js          # Emotion mapping
├── App.jsx                       # Main app
├── main.jsx                      # Entry point
└── index.css                     # Global styles
```

## 🎯 Key Components

### useChat Hook

Manages WebSocket connection and message handling:

```javascript
const { 
  sendMessage, 
  resetConversation, 
  isConnected 
} = useChat();
```

### AgentMessageBubble

Displays AI messages with:
- Vietnamese translation
- Chinese content (clickable characters)
- Pinyin
- Emotion badges
- Interactive quizzes
- Correction highlighting

### HanziPlayer

Animates Chinese character strokes:
- Auto-play animation
- Manual control buttons
- Practice mode (quiz)

## 🎨 Wuxia Design System

### Colors

```javascript
// Parchment (Paper)
bg-parchment-50, bg-parchment-100, bg-parchment-200

// Ink (Text)
text-ink-800, text-ink-900

// Cinnabar (Accents)
text-cinnabar-600, text-cinnabar-700, bg-cinnabar-700
```

### Fonts

```css
font-serif      /* Vietnamese text */
font-chinese    /* Chinese characters */
font-kaiti      /* Calligraphy style */
```

### Custom Effects

```css
brush-border         /* Brush stroke effect */
scrollbar-wuxia      /* Custom scrollbar */
chinese-char         /* Clickable characters */
message-bubble       /* Bubble animation */
emotion-pulse        /* Emotion badge pulse */
```

## 🔧 Configuration

### Backend URL

Change WebSocket URL in `src/hooks/useChat.js`:

```javascript
const WS_URL = `ws://localhost:8000/ws/chat/${userId}/`;
```

### Audio Settings

Modify in `src/utils/audioPlayer.js`:

```javascript
audio.volume = 1.0; // Volume (0.0 - 1.0)
```

## 📱 Responsive Breakpoints

- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

## 🎮 User Interactions

### Click Chinese Character
Opens HanziModal with stroke animation

### Send Message
- Enter key (desktop)
- Send button (all devices)

### Quick Suggestions
Pre-filled message buttons below input

### Audio Toggle
Enable/disable TTS audio playback

### Settings
- Change user role (师兄/师姐/etc.)
- View sulking level

## 🧪 Testing

```bash
# Run linter
npm run lint
```

## 🐛 Common Issues

### Audio Not Playing

**Issue**: Browser blocks autoplay

**Solution**: Click "Bắt đầu học" button to unlock audio

### WebSocket Connection Failed

**Issue**: Backend not running

**Solution**: Start Django backend:
```bash
cd backend
daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

### Characters Not Clickable

**Issue**: HanziWriter data not loaded

**Solution**: Check internet connection (loads from CDN)

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

Output in `dist/` folder

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod
```

## 🎓 Key Technologies

- **React 18** - UI framework
- **Vite** - Build tool
- **Zustand** - State management
- **Tailwind CSS** - Styling
- **react-use-websocket** - WebSocket client
- **hanzi-writer** - Character animation
- **lucide-react** - Icons

## 📝 Customization

### Change Theme Colors

Edit `tailwind.config.js`:

```javascript
colors: {
  parchment: { /* your colors */ },
  cinnabar: { /* your colors */ },
}
```

### Add New Emotions

Edit `src/utils/emotionHelper.js`:

```javascript
export const EMOTION_EMOJIS = {
  // Add new emotion
  playful: '😜',
};
```

### Modify Chat Bubbles

Edit components in `src/components/`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

[Add your license]

---

**Made with ❤️ for Chinese language learners**

祝你学习愉快！(Zhù nǐ xuéxí yúkuài!)
