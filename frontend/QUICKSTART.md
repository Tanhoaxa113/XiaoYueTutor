# XiaoYue Frontend - Quick Start Guide

Get your beautiful Wuxia-themed chat interface running in 5 minutes! 📜

## 🚀 Installation & Setup

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

This will install:
- React 18
- Vite
- Tailwind CSS
- Zustand (state management)
- react-use-websocket
- hanzi-writer
- lucide-react (icons)

### Step 2: Start Development Server

```bash
npm run dev
```

Frontend will be available at: **http://localhost:3000**

### Step 3: Ensure Backend is Running

The frontend needs the Django backend WebSocket server:

```bash
# In backend directory
cd ../backend
daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

Backend WebSocket: **ws://localhost:8000/ws/chat/**

## 🎯 First Run Experience

1. Open **http://localhost:3000** in your browser
2. You'll see a beautiful start overlay with "小师妹" title
3. Click **"Bắt đầu học"** button to unlock audio
4. Start chatting!

## 💬 Try These Messages

```
你好，小师妹
Dạy em nói "cảm ơn"
Giải thích chữ "爱" cho em
我今天很高心 (intentional error for correction)
```

## 🎨 Key Features

### 1. **Real-time Chat**
- WebSocket connection to Django backend
- Instant message delivery
- Typing indicators

### 2. **Audio Playback**
- Automatic TTS audio from Base64
- Sequential queue (no overlapping)
- Volume toggle button

### 3. **Hanzi Animation**
- Click any Chinese character in messages
- Beautiful stroke-by-stroke animation
- Practice mode for writing

### 4. **Interactive Quizzes**
- Multiple choice questions
- Fill-in-the-blank exercises
- Instant feedback

### 5. **Emotion Display**
- AI emotion states (happy, sulking, angry, etc.)
- Emoji indicators
- Sulking level (0-3)

### 6. **User Roles**
- 师兄 (Sư Huynh) - Senior Brother
- 师姐 (Sư Tỷ) - Senior Sister
- 师弟 (Sư Đệ) - Junior Brother
- 师妹 (Sư Muội) - Junior Sister

## 🖼️ UI Components

### Chat Header
- Agent name and avatar
- Emotion display
- Connection status
- Settings button
- Reset button

### Message Bubbles
- **Agent (Left)**: Vietnamese + Chinese + Pinyin + Quizzes
- **User (Right)**: Simple, elegant design
- Clickable Chinese characters
- Timestamps

### Chat Input
- Text input area
- Audio toggle
- Mic button (placeholder)
- Send button
- Quick suggestions

### Modals
- **Hanzi Modal**: Character stroke animation
- **Settings Modal**: User role selection

## ⚙️ Configuration

### Change Backend URL

Edit `src/hooks/useChat.js`:

```javascript
const WS_URL = `ws://your-backend-url/ws/chat/${userId}/`;
```

### Adjust Colors

Edit `tailwind.config.js`:

```javascript
colors: {
  parchment: {
    100: '#f9f5ed', // Main background
  },
  cinnabar: {
    700: '#b91c1c', // Primary accent
  },
}
```

### Modify Fonts

Edit `index.html` (Google Fonts):

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif:wght@400;600;700&display=swap" rel="stylesheet">
```

## 🐛 Troubleshooting

### Issue: "WebSocket connection failed"

**Solution**: Make sure Django backend is running on port 8000

```bash
cd backend
daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

### Issue: "Audio not playing"

**Solution**: Click the "Bắt đầu học" button first (browser autoplay policy)

Also check the audio toggle button (volume icon) is ON

### Issue: "Chinese characters not animating"

**Solution**: 
1. Check internet connection (hanzi-writer loads from CDN)
2. Try a simpler character like "爱" or "人"
3. Check browser console for errors

### Issue: "Messages not sending"

**Solution**:
1. Check WebSocket connection status in header
2. Verify backend is running
3. Check browser console for errors

## 📱 Responsive Design

The interface works beautifully on:
- 📱 Mobile (portrait & landscape)
- 📱 Tablets
- 💻 Desktop
- 🖥️ Large screens

## 🎮 Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line in input
- **Esc**: Close modals

## 🎨 Wuxia Design Elements

### Paper Texture
Subtle grid pattern on background

### Brush Borders
Soft, artistic borders on message bubbles

### Chinese Decorations
Large watermark characters (武侠) in background

### Color Palette
- 📜 Parchment (paper tones)
- 🖋️ Ink (deep blacks)
- 🔴 Cinnabar (red accents)

## 🚀 Build for Production

```bash
npm run build
```

Output in `dist/` folder

Serve with any static hosting:
- Vercel
- Netlify
- GitHub Pages
- Nginx

## 📊 Project Stats

- **Components**: 11 files
- **Hooks**: 1 custom hook
- **Utils**: 2 helper files
- **Lines of Code**: ~1,500 lines
- **Bundle Size**: ~200KB (gzipped)

## 🎯 Next Steps

### Customization Ideas

1. **Add more emotions**
   - Edit `src/utils/emotionHelper.js`
   - Add emoji and color mappings

2. **Custom quiz types**
   - Edit `src/components/AgentMessageBubble.jsx`
   - Add new quiz rendering logic

3. **User authentication**
   - Add login page
   - Store user ID in localStorage
   - Send auth token with WebSocket

4. **Learning progress**
   - Track completed quizzes
   - Show statistics dashboard
   - Save vocabulary lists

5. **Dark mode**
   - Add theme toggle
   - Update Tailwind config
   - Store preference

## 📚 Learn More

- [React Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Vite](https://vitejs.dev)
- [Zustand](https://zustand-demo.pmnd.rs)
- [hanzi-writer](https://chanind.github.io/hanzi-writer/)

## 🤝 Need Help?

Check:
1. Browser console (F12)
2. Network tab for WebSocket
3. Backend logs
4. README.md for detailed docs

## ✨ Tips

1. **Performance**: React DevTools to check re-renders
2. **Debugging**: Use `console.log` in useChat hook
3. **Styling**: Use Tailwind IntelliSense VSCode extension
4. **Testing**: Test with different user roles and emotions

---

**Enjoy building your Wuxia learning experience!** 🥋

学习愉快！(Xuéxí yúkuài!)

