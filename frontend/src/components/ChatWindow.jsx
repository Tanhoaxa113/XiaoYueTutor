import { useEffect, useRef } from 'react';
import useChatStore from '../store/chatStore';
import AgentMessageBubble from './AgentMessageBubble';
import UserMessageBubble from './UserMessageBubble';

/**
 * Main chat message display area
 */
const ChatWindow = () => {
  const { messages, isTyping } = useChatStore();
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className="flex-1 overflow-y-auto scrollbar-wuxia scroll-shadow p-4 space-y-4">
      <div className="max-w-4xl mx-auto space-y-4">
        {/* Welcome message */}
        {messages.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📜</div>
            <h2 className="text-2xl font-chinese text-ink-900 mb-2">
              欢迎！ Chào mừng!
            </h2>
            <p className="text-stone-600 font-serif">
              Bắt đầu cuộc trò chuyện với Tiểu Sư Muội để học tiếng Trung
            </p>
            <div className="mt-6 p-4 bg-amber-50 border-2 border-amber-200 rounded-lg max-w-md mx-auto text-left">
              <p className="text-sm text-stone-700 font-serif mb-2">
                <strong>💡 Gợi ý:</strong>
              </p>
              <ul className="text-sm text-stone-600 font-serif space-y-1 list-disc list-inside">
                <li>Chào Tiểu Sư Muội</li>
                <li>Dạy em nói "xin chào"</li>
                <li>Tôi muốn học số đếm</li>
                <li>Giải thích chữ "爱" cho em</li>
              </ul>
            </div>
          </div>
        )}

        {/* Messages */}
        {messages.map((msg) => {
          if (msg.role === 'user') {
            return <UserMessageBubble key={msg.id} message={msg} />;
          } else if (msg.role === 'assistant') {
            return <AgentMessageBubble key={msg.id} message={msg} />;
          } else if (msg.role === 'system') {
            return (
              <div key={msg.id} className="text-center">
                <p className="inline-block px-4 py-2 bg-stone-200 text-stone-700 rounded-full text-sm font-serif">
                  {msg.content}
                </p>
              </div>
            );
          }
          return null;
        })}

        {/* Typing indicator */}
        {isTyping && (
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-pink-300 to-pink-400 flex items-center justify-center text-white text-xl shadow-md">
              💭
            </div>
            <div className="bg-white border-2 border-stone-200 rounded-2xl rounded-tl-none p-4 shadow-md">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-stone-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-stone-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-stone-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatWindow;

