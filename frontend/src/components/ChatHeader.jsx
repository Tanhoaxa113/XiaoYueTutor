import { Settings, RefreshCw, Wifi, WifiOff } from 'lucide-react';
import useChatStore from '../store/chatStore';
import { getEmotionDisplay, getSulkingDescription } from '../utils/emotionHelper';

/**
 * Chat header with agent status and controls
 */
const ChatHeader = ({ onSettingsClick, onResetClick, isConnected }) => {
  const { agentRole, agentEmotion, sulkingLevel, isTyping } = useChatStore();
  const emotionDisplay = getEmotionDisplay(agentEmotion);

  return (
    <div className="bg-gradient-to-r from-parchment-100 to-parchment-200 border-b-4 border-stone-300 p-4 shadow-md">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        {/* Agent info */}
        <div className="flex items-center gap-4">
          {/* Avatar */}
          <div className="relative">
            <div className="w-14 h-14 rounded-full bg-gradient-to-br from-pink-300 to-pink-400 flex items-center justify-center text-white text-2xl shadow-lg">
              {emotionDisplay.emoji}
            </div>
            {/* Connection indicator */}
            <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full border-2 border-white ${
              isConnected ? 'bg-green-500' : 'bg-red-500'
            }`} />
          </div>

          {/* Agent name and status */}
          <div>
            <h1 className="text-xl font-chinese font-bold text-ink-900 flex items-center gap-2">
              {agentRole}
              <span className="text-base font-serif text-stone-600">• Tiểu Sư Muội</span>
            </h1>
            
            {isTyping ? (
              <p className="text-sm text-stone-600 font-serif italic animate-pulse">
                Đang nhập...
              </p>
            ) : (
              <div className="flex items-center gap-2 text-sm font-serif">
                <span className={emotionDisplay.color}>{emotionDisplay.text}</span>
                <span className="text-stone-400">•</span>
                <span className="text-stone-600">{getSulkingDescription(sulkingLevel)}</span>
              </div>
            )}
          </div>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-2">
          {/* Connection status */}
          <div className={`flex items-center gap-1 px-3 py-1 rounded-full text-xs font-serif ${
            isConnected 
              ? 'bg-green-100 text-green-700' 
              : 'bg-red-100 text-red-700'
          }`}>
            {isConnected ? (
              <>
                <Wifi className="w-3 h-3" />
                <span>Kết nối</span>
              </>
            ) : (
              <>
                <WifiOff className="w-3 h-3" />
                <span>Mất kết nối</span>
              </>
            )}
          </div>

          {/* Reset button */}
          <button
            onClick={onResetClick}
            className="p-2 hover:bg-stone-200 rounded-lg transition-colors group"
            title="Làm mới cuộc trò chuyện"
          >
            <RefreshCw className="w-5 h-5 text-stone-600 group-hover:text-stone-800 group-hover:rotate-180 transition-all duration-300" />
          </button>

          {/* Settings button */}
          <button
            onClick={onSettingsClick}
            className="p-2 hover:bg-stone-200 rounded-lg transition-colors group"
            title="Cài đặt"
          >
            <Settings className="w-5 h-5 text-stone-600 group-hover:text-stone-800 group-hover:rotate-90 transition-all duration-300" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatHeader;

