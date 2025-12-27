import { X } from 'lucide-react';
import useChatStore from '../store/chatStore';

/**
 * Settings modal for user preferences
 */
const SettingsModal = ({ isOpen, onClose }) => {
  const { userRole, setUserRole, sulkingLevel } = useChatStore();

  if (!isOpen) return null;

  const roles = [
    { value: 'Sư huynh', label: 'Sư huynh (师兄)', description: 'Senior Brother - Agent: Muội muội (Playful/Tsundere)' },
    { value: 'Muội muội', label: 'Muội muội (妹妹)', description: 'Younger Sister - Agent: Tỷ tỷ (Caring/Strict)' },
    { value: 'Đệ đệ', label: 'Đệ đệ (弟弟)', description: 'Younger Brother - Agent: Tỷ tỷ ác ma (Demon Sister)' },
    { value: 'Tỷ tỷ', label: 'Tỷ tỷ (姐姐)', description: 'Older Sister - Agent: Muội muội (Sweet/Clingy)' },
  ];

  return (
    <div 
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div 
        className="bg-parchment-100 rounded-2xl shadow-2xl max-w-lg w-full p-6 relative animate-character-appear"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-chinese text-ink-900">
            设置 • Cài đặt
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-stone-200 rounded-lg transition-colors"
            aria-label="Close"
          >
            <X className="w-5 h-5 text-stone-600" />
          </button>
        </div>

        {/* User role selection */}
        <div className="mb-6">
          <h3 className="text-lg font-serif font-semibold text-stone-800 mb-3">
            Vai trò của bạn
          </h3>
          <div className="space-y-2">
            {roles.map((role) => (
              <button
                key={role.value}
                onClick={() => setUserRole(role.value)}
                className={`w-full text-left p-4 rounded-xl border-2 transition-all ${
                  userRole === role.value
                    ? 'border-cinnabar-600 bg-cinnabar-50'
                    : 'border-stone-300 bg-white hover:border-stone-400'
                }`}
              >
                <div className="font-chinese text-lg text-ink-900 mb-1">
                  {role.label}
                </div>
                <div className="text-sm text-stone-600 font-serif">
                  {role.description}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Sulking level display */}
        <div className="mb-6 p-4 bg-amber-50 border-2 border-amber-200 rounded-xl">
          <h3 className="text-lg font-serif font-semibold text-stone-800 mb-2">
            Tâm trạng của Tiểu Sư Muội
          </h3>
          <div className="flex items-center gap-3">
            <div className="text-3xl">
              {sulkingLevel === 0 && '😊'}
              {sulkingLevel === 1 && '😤'}
              {sulkingLevel === 2 && '😠'}
              {sulkingLevel === 3 && '😡'}
            </div>
            <div>
              <div className="font-serif text-stone-700">
                Mức dỗi: <strong>{sulkingLevel}/3</strong>
              </div>
              <div className="text-sm text-stone-600 font-serif">
                {sulkingLevel === 0 && 'Vui vẻ, sẵn sàng dạy học'}
                {sulkingLevel === 1 && 'Hơi dỗi, nhưng vẫn dạy'}
                {sulkingLevel === 2 && 'Đang dỗi, nói chuyện có gai'}
                {sulkingLevel === 3 && 'Rất giận, không muốn dạy'}
              </div>
            </div>
          </div>
        </div>

        {/* Info */}
        <div className="p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
          <p className="text-sm text-stone-700 font-serif">
            <strong>💡 Lưu ý:</strong> Vai trò của bạn ảnh hưởng đến cách Tiểu Sư Muội 
            xưng hô và phong cách dạy học!
          </p>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;

