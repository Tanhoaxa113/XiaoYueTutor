import { useState } from 'react';
import useChat from './hooks/useChat';
import ChatHeader from './components/ChatHeader';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import HanziModal from './components/HanziModal';
import SettingsModal from './components/SettingsModal';
import StartOverlay from './components/StartOverlay';
import useChatStore from './store/chatStore';

/**
 * Main App component
 */
function App() {
  const [showSettings, setShowSettings] = useState(false);
  const { sendMessage, resetConversation, isConnected } = useChat();
  const { clearMessages } = useChatStore();

  const handleReset = () => {
    if (confirm('Bạn có chắc muốn làm mới cuộc trò chuyện?')) {
      clearMessages();
      resetConversation();
    }
  };

  return (
    <div className="h-screen flex flex-col bg-parchment-50">
      {/* Start overlay */}
      <StartOverlay />

      {/* Header */}
      <ChatHeader
        onSettingsClick={() => setShowSettings(true)}
        onResetClick={handleReset}
        isConnected={isConnected}
      />

      {/* Chat window */}
      <ChatWindow />

      {/* Input area */}
      <ChatInput
        onSendMessage={sendMessage}
        disabled={!isConnected}
      />

      {/* Modals */}
      <HanziModal />
      <SettingsModal
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
      />

      {/* Decorative elements */}
      <div className="fixed top-20 right-10 opacity-5 pointer-events-none">
        <div className="text-9xl font-chinese text-stone-400">武</div>
      </div>
      <div className="fixed bottom-20 left-10 opacity-5 pointer-events-none">
        <div className="text-9xl font-chinese text-stone-400">侠</div>
      </div>
    </div>
  );
}

export default App;
