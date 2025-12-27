import { X } from 'lucide-react';
import useChatStore from '../store/chatStore';
import HanziPlayer from './HanziPlayer';

/**
 * Modal component for displaying Hanzi character animation
 */
const HanziModal = () => {
  const { showHanziModal, selectedCharacter, closeHanziModal } = useChatStore();

  if (!showHanziModal || !selectedCharacter) return null;

  return (
    <div 
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={closeHanziModal}
    >
      <div 
        className="bg-parchment-100 rounded-2xl shadow-2xl max-w-md w-full p-6 relative animate-character-appear"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-chinese text-ink-900">
            学习汉字 • Học Hán Tự
          </h2>
          <button
            onClick={closeHanziModal}
            className="p-2 hover:bg-stone-200 rounded-lg transition-colors"
            aria-label="Close"
          >
            <X className="w-5 h-5 text-stone-600" />
          </button>
        </div>

        {/* Character display */}
        <div className="mb-4 text-center">
          <div className="text-7xl font-chinese text-ink-900 mb-2">
            {selectedCharacter}
          </div>
          <p className="text-sm text-stone-600 font-serif">
            Nhấn các nút bên dưới để xem nét viết
          </p>
        </div>

        {/* Hanzi Player */}
        <HanziPlayer 
          character={selectedCharacter}
          size={250}
          autoAnimate={true}
        />

        {/* Tips */}
        <div className="mt-6 p-4 bg-amber-50 border-l-4 border-amber-500 rounded-r-lg">
          <p className="text-xs text-stone-700 font-serif">
            <strong>💡 Mẹo:</strong> Nhấn "Luyện viết" để tự vẽ theo thứ tự nét!
          </p>
        </div>
      </div>
    </div>
  );
};

export default HanziModal;

