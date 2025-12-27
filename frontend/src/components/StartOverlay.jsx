import { Volume2 } from 'lucide-react';
import useChatStore from '../store/chatStore';
import { initAudioContext } from '../utils/audioPlayer';

/**
 * Start overlay to unlock audio (browser autoplay policy)
 */
const StartOverlay = () => {
  const { audioUnlocked, setAudioUnlocked } = useChatStore();

  const handleStart = () => {
    // Initialize audio context on user gesture
    initAudioContext();
    setAudioUnlocked(true);
  };

  if (audioUnlocked) return null;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-parchment-100 rounded-2xl shadow-2xl max-w-md w-full p-8 text-center animate-character-appear">
        {/* Icon */}
        <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-pink-300 to-pink-400 flex items-center justify-center text-4xl shadow-lg">
          📜
        </div>

        {/* Title */}
        <h1 className="text-3xl font-chinese text-ink-900 mb-2">
          小师妹
        </h1>
        <p className="text-xl font-serif text-stone-700 mb-6">
          Tiểu Sư Muội - Học Tiếng Trung
        </p>

        {/* Description */}
        <p className="text-stone-600 font-serif mb-8 leading-relaxed">
          Chào mừng bạn đến với lớp học tiếng Trung phong cách Cổ Trang! 
          Hãy nhấn nút bên dưới để bắt đầu và kích hoạt âm thanh.
        </p>

        {/* Start button */}
        <button
          onClick={handleStart}
          className="w-full py-4 bg-gradient-to-r from-cinnabar-700 to-cinnabar-800 text-white rounded-xl font-serif text-lg font-semibold hover:from-cinnabar-800 hover:to-cinnabar-900 transition-all shadow-lg hover:shadow-xl transform hover:scale-105 flex items-center justify-center gap-2"
        >
          <Volume2 className="w-6 h-6" />
          <span>Bắt đầu học</span>
        </button>

        {/* Features */}
        <div className="mt-8 pt-6 border-t-2 border-stone-200">
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <div className="text-2xl mb-1">🎤</div>
              <p className="text-stone-600 font-serif">Phát âm</p>
            </div>
            <div>
              <div className="text-2xl mb-1">✍️</div>
              <p className="text-stone-600 font-serif">Viết chữ</p>
            </div>
            <div>
              <div className="text-2xl mb-1">📝</div>
              <p className="text-stone-600 font-serif">Bài tập</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StartOverlay;

