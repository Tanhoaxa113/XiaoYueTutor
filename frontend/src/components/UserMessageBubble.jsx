/**
 * User message bubble (right-aligned)
 */
const UserMessageBubble = ({ message }) => {
  const { content } = message;

  return (
    <div className="flex items-start gap-3 justify-end message-bubble">
      {/* Message content */}
      <div className="max-w-[80%]">
        {/* Main bubble */}
        <div className="bg-gradient-to-br from-stone-700 to-stone-800 rounded-2xl rounded-tr-none p-4 shadow-md">
          <p className="text-base font-serif text-white leading-relaxed">
            {content}
          </p>
        </div>

        {/* Timestamp */}
        <p className="text-xs text-stone-400 mt-1 mr-2 text-right font-serif">
          {new Date(message.timestamp).toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>

      {/* Avatar */}
      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-stone-600 to-stone-700 flex items-center justify-center text-white text-lg shadow-md font-chinese">
        师
      </div>
    </div>
  );
};

export default UserMessageBubble;

