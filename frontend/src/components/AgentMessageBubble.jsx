import { useState } from 'react';
import { CheckCircle2, XCircle, Sparkles, Volume2, Loader2 } from 'lucide-react';
import useChatStore from '../store/chatStore';
import { getEmotionDisplay } from '../utils/emotionHelper';
import { playAudioFromBase64 } from '../utils/audioPlayer';

/**
 * Agent (AI) message bubble with Vietnamese text, pinyin, and interactive features
 */
const AgentMessageBubble = ({ message }) => {
  const { openHanziModal, audioVolume } = useChatStore();
  const [quizAnswers, setQuizAnswers] = useState({});
  const [showQuizResults, setShowQuizResults] = useState({});
  const [isPlaying, setIsPlaying] = useState(false);
  const {
    content,
    chinese_content,
    pinyin,
    emotion = 'neutral',
    action,
    correction_detail,
    quiz_list = [],
    audio_base64,
  } = message;

  const emotionDisplay = getEmotionDisplay(emotion);
  const handlePlayAudio = async () => {
    if (!audio_base64 || isPlaying) return;
    
    setIsPlaying(true);
    try {
      await playAudioFromBase64(audio_base64, audioVolume);
    } catch (error) {
      console.error("Lỗi phát audio:", error);
    } finally {
      setIsPlaying(false);
    }
  };
  // Handle clicking on Chinese characters
  const handleCharacterClick = (char) => {
    // Only Chinese characters (U+4E00 to U+9FFF)
    if (/[\u4E00-\u9FFF]/.test(char)) {
      openHanziModal(char);
    }
  };

  // Render Chinese content with clickable characters
  const renderChineseContent = () => {
    if (!chinese_content) return null;

    return (
      <div className="text-lg font-chinese text-ink-900 mb-2 leading-relaxed">
        {chinese_content.split('').map((char, idx) => {
          if (/[\u4E00-\u9FFF]/.test(char)) {
            return (
              <span
                key={idx}
                className="chinese-char"
                onClick={() => handleCharacterClick(char)}
                title="Nhấn để xem nét viết"
              >
                {char}
              </span>
            );
          }
          return <span key={idx}>{char}</span>;
        })}
      </div>
    );
  };

  // Handle quiz submission
  const handleQuizSubmit = (quizId, userAnswer, correctAnswer) => {
    if (!userAnswer) return; // Chặn nếu chưa nhập gì

    // Chuẩn hóa câu trả lời: bỏ khoảng trắng thừa, viết thường
    const normalizedUser = userAnswer.toString().trim().toLowerCase();
    const normalizedCorrect = correctAnswer.toString().trim().toLowerCase();
    
    // So sánh linh hoạt hơn (ví dụ: chấp nhận cả dấu câu nếu cần)
    const isCorrect = normalizedUser === normalizedCorrect;
    
    // Cập nhật state để hiện kết quả
    setShowQuizResults(prev => ({
      ...prev,
      [quizId]: isCorrect,
    }));
    
    // (Optional) Nếu muốn phát âm thanh chúc mừng/chia buồn thì gọi store ở đây
    // if (isCorrect) playSound('correct'); 
  };

  // Render quiz
  const renderQuiz = () => {
    if (!quiz_list || quiz_list.length === 0) return null;

    return (
      <div className="mt-4 space-y-4">
        <div className="flex items-center gap-2 text-cinnabar-700 font-semibold">
          <Sparkles className="w-4 h-4" />
          <span className="font-serif">Bài tập</span>
        </div>

        {quiz_list.map((quiz, idx) => {
          const quizId = quiz.id || idx;
          const userAnswer = quizAnswers[quizId] || '';
          const showResult = showQuizResults[quizId] !== undefined;

          return (
            <div key={quizId} className="bg-amber-50 border-2 border-amber-200 rounded-lg p-4">
              {/* Question */}
              <p className="font-serif font-semibold text-stone-800 mb-3">
                {idx + 1}. {quiz.question}
              </p>

              {/* Multiple choice */}
              {quiz.type === 'multiple_choice' && quiz.options && (
                <div className="space-y-2">
                  {quiz.options.map((option, optIdx) => (
                    <button
                      key={optIdx}
                      onClick={() => {
                        setQuizAnswers({ ...quizAnswers, [quizId]: option });
                        handleQuizSubmit(quizId, option, quiz.answer);
                      }}
                      disabled={showResult}
                      className={`w-full text-left p-3 rounded-md border-2 transition-all font-serif ${showResult
                          ? option === quiz.answer
                            ? 'border-green-500 bg-green-50'
                            : userAnswer === option
                              ? 'border-red-500 bg-red-50'
                              : 'border-stone-200 bg-white'
                          : 'border-stone-300 bg-white hover:border-stone-400 hover:bg-stone-50'
                        }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              )}

              {/* Fill in the blank */}
              {quiz.type === 'fill_blank' && (
                <div className="space-y-2">
                  <input
                    type="text"
                    value={userAnswer}
                    // Thêm sự kiện onKeyPress để Enter là submit luôn cho tiện
                    onKeyPress={(e) => {
                        if (e.key === 'Enter') handleQuizSubmit(quizId, userAnswer, quiz.answer);
                    }}
                    onChange={(e) => {
                        // Cập nhật state nhập liệu
                        setQuizAnswers(prev => ({ ...prev, [quizId]: e.target.value }));
                    }}
                    placeholder="Nhập câu trả lời..."
                    disabled={showResult} // Disable khi đã nộp bài
                    className="w-full p-3 border-2 border-stone-300 rounded-md focus:outline-none focus:border-cinnabar-600 font-serif"
                  />
                  
                  {/* Nút kiểm tra: Chỉ hiện khi CHƯA có kết quả */}
                  {!showResult && (
                    <button
                      onClick={(e) => {
                          e.stopPropagation(); // Ngăn sự kiện click lan ra ngoài bubble
                          handleQuizSubmit(quizId, userAnswer, quiz.answer);
                      }}
                      // Disable nút nếu chưa nhập gì để tránh bấm nhầm
                      disabled={!userAnswer} 
                      className={`px-4 py-2 text-white rounded-md transition-colors font-serif ${
                          !userAnswer 
                          ? 'bg-stone-400 cursor-not-allowed' 
                          : 'bg-cinnabar-700 hover:bg-cinnabar-800'
                      }`}
                    >
                      Kiểm tra
                    </button>
                  )}
                </div>
              )}

              {/* Result */}
              {showResult && (
                <div className={`mt-3 p-3 rounded-md flex items-center gap-2 ${showQuizResults[quizId]
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                  }`}>
                  {showQuizResults[quizId] ? (
                    <>
                      <CheckCircle2 className="w-5 h-5" />
                      <span className="font-serif font-semibold">Chính xác!</span>
                    </>
                  ) : (
                    <>
                      <XCircle className="w-5 h-5" />
                      <span className="font-serif">
                        Sai rồi! Đáp án đúng: <strong>{quiz.answer}</strong>
                      </span>
                    </>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    );
  };

  // Render correction highlighting
  const renderCorrection = () => {
    // Ưu tiên 1: Cách mới (Xịn) - Chỉ hiện khi có object correction_detail
    if (action === 'correction' && correction_detail && !correction_detail.is_correct) {
      return (
        <div className="mt-3 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg space-y-2 animate-pulse-subtle">
          {/* Hiện lỗi sai */}
          {correction_detail.mistake_highlight && (
            <div className="flex items-start gap-2">
              <span className="text-red-600 font-bold min-w-[60px] text-sm font-serif">❌ Lỗi:</span>
              <span className="text-stone-600 line-through decoration-red-400 decoration-2 font-chinese">
                {correction_detail.mistake_highlight}
              </span>
            </div>
          )}

          {/* Hiện giải thích */}
          <div className="flex items-start gap-2">
            <span className="text-green-700 font-bold min-w-[60px] text-sm font-serif">💡 Sửa:</span>
            <span className="text-stone-800 text-sm font-serif italic">
              {correction_detail.explanation}
            </span>
          </div>
        </div>
      );
    }

    // Ưu tiên 2: Fallback (Chỉ chạy khi KHÔNG CÓ correction_detail VÀ action là correction)
    // Lưu ý: Muội phải dùng !correction_detail ở đây để tránh hiển thị trùng lặp
    if (action === 'correction' && !correction_detail) {
      return (
        <div className="mt-2 p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg">
          <p className="text-sm text-red-800 font-serif">
            <span className="font-semibold">⚠️ Sửa lỗi:</span>
            {/* Fallback thì đành hiện content đỡ, hoặc hiện thông báo generic */}
            Có lỗi ngữ pháp trong câu của bạn.
          </p>
        </div>
      );
    }

    return null;
  };
  return (
    <div className="flex items-start gap-3 message-bubble">
      {/* Avatar */}
      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-pink-300 to-pink-400 flex items-center justify-center text-white text-xl shadow-md">
        {emotionDisplay.emoji}
      </div>

      {/* Message content */}
      <div className="flex-1 max-w-[80%]">
        {/* Main bubble */}
        <div className="bg-white border-2 border-stone-200 rounded-2xl rounded-tl-none p-4 shadow-scroll brush-border">
          {/* Vietnamese display */}
          <p className="text-base font-serif text-stone-800 leading-relaxed mb-2">
            {content}
          </p>

          {/* Chinese content (clickable) */}
          {renderChineseContent()}

          {/* Pinyin */}
          {pinyin && (
            <p className="text-sm text-stone-500 italic font-serif mt-1">
              {pinyin}
            </p>
          )}

          <div className="flex items-center gap-2 mt-2">
            
            {/* Emotion Badge cũ */}
            <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs ${emotionDisplay.color} bg-stone-100 emotion-pulse`}>
              <span>{emotionDisplay.emoji}</span>
              <span className="font-serif">{emotionDisplay.text}</span>
            </div>

            {/* --- NÚT PHÁT LẠI MỚI --- */}
            {audio_base64 && (
              <button
                onClick={handlePlayAudio}
                disabled={isPlaying}
                className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs transition-all border border-stone-200 
                  ${isPlaying 
                    ? 'bg-cinnabar-100 text-cinnabar-700' 
                    : 'bg-stone-50 text-stone-600 hover:bg-stone-200 hover:text-stone-800'
                  }`}
                title="Nghe lại"
              >
                {isPlaying ? (
                  <Loader2 className="w-3 h-3 animate-spin" />
                ) : (
                  <Volume2 className="w-3 h-3" />
                )}
                <span className="font-serif">Nghe</span>
              </button>
            )}
            
          </div>

          {/* Correction */}
          {renderCorrection()}

          {/* Quiz */}
          {renderQuiz()}
        </div>

        {/* Timestamp */}
        <p className="text-xs text-stone-400 mt-1 ml-2 font-serif">
          {new Date(message.timestamp).toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
    </div>
  );
};

export default AgentMessageBubble;

