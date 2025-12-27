import { useState } from 'react';
import { Send, Mic, Volume2, VolumeX } from 'lucide-react';
import useChatStore from '../store/chatStore';

/**
 * Chat input area with send button and mic button
 */
const ChatInput = ({ onSendMessage, disabled }) => {
  const [inputText, setInputText] = useState('');
  const { audioUnlocked, setAudioUnlocked, audioVolume, setAudioVolume } = useChatStore();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim() || disabled) return;

    onSendMessage(inputText);
    setInputText('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="bg-parchment-100 border-t-4 border-stone-300 p-4 shadow-lg">
      <div className="max-w-4xl mx-auto">
        <form onSubmit={handleSubmit} className="flex items-end gap-3">
          {/* Audio toggle */}
          <div className="flex items-center bg-stone-200 rounded-xl p-1 transition-all">
            {/* Nút Mute/Unmute */}
            <button
              type="button"
              onClick={() => setAudioUnlocked(!audioUnlocked)}
              className={`flex-shrink-0 p-2 rounded-lg transition-all ${
                audioUnlocked
                  ? 'bg-green-100 text-green-700 hover:bg-green-200'
                  : 'text-stone-500 hover:bg-stone-300'
              }`}
              title={audioUnlocked ? 'Tắt âm thanh' : 'Bật âm thanh'}
            >
              {audioUnlocked ? (
                <Volume2 className="w-5 h-5" />
              ) : (
                <VolumeX className="w-5 h-5" />
              )}
            </button>

            {/* Thanh trượt Volume (Chỉ hiện khi bật tiếng) */}
            {audioUnlocked && (
              <div className="w-20 px-2 animate-in fade-in slide-in-from-left-2 duration-200">
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={audioVolume}
                  onChange={(e) => setAudioVolume(parseFloat(e.target.value))}
                  className="w-full h-1 bg-stone-400 rounded-lg appearance-none cursor-pointer accent-cinnabar-700"
                  title={`Âm lượng: ${Math.round(audioVolume * 100)}%`}
                />
              </div>
            )}
          </div>

          {/* Text input */}
          <div className="flex-1 relative">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Nhập tin nhắn... (Enter để gửi)"
              disabled={disabled}
              rows={1}
              className="w-full px-4 py-3 pr-12 bg-white border-2 border-stone-300 rounded-xl focus:outline-none focus:border-cinnabar-600 resize-none font-serif text-stone-800 placeholder:text-stone-400 disabled:bg-stone-100 disabled:cursor-not-allowed"
              style={{
                minHeight: '50px',
                maxHeight: '120px',
              }}
            />
          </div>

          {/* Mic button (placeholder) */}
          <button
            type="button"
            className="flex-shrink-0 p-3 bg-stone-200 text-stone-600 rounded-xl hover:bg-stone-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={disabled}
            title="Nhập bằng giọng nói (sắp ra mắt)"
          >
            <Mic className="w-5 h-5" />
          </button>

          {/* Send button */}
          <button
            type="submit"
            disabled={!inputText.trim() || disabled}
            className="flex-shrink-0 p-3 bg-gradient-to-r from-cinnabar-700 to-cinnabar-800 text-white rounded-xl hover:from-cinnabar-800 hover:to-cinnabar-900 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>

        {/* Quick suggestions */}
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            onClick={() => setInputText('你好，小师妹')}
            className="px-3 py-1 bg-stone-200 text-stone-700 rounded-full text-sm font-serif hover:bg-stone-300 transition-colors"
          >
            你好
          </button>
          <button
            onClick={() => setInputText('Dạy em nói "cảm ơn"')}
            className="px-3 py-1 bg-stone-200 text-stone-700 rounded-full text-sm font-serif hover:bg-stone-300 transition-colors"
          >
            Dạy nói "cảm ơn"
          </button>
          <button
            onClick={() => setInputText('Giải thích chữ "爱" cho em')}
            className="px-3 py-1 bg-stone-200 text-stone-700 rounded-full text-sm font-serif hover:bg-stone-300 transition-colors"
          >
            Giải thích chữ Hán
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;

