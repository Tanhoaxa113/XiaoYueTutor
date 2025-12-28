import { useEffect, useRef, useCallback } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import useChatStore from '../store/chatStore';
import { playAudioFromBase64 } from '../utils/audioPlayer';
/**
 * Custom hook for WebSocket chat connection and message handling
 */
const useChat = () => {
  const {
    userId,
    userRole,
    addMessage,
    setAgentState,
    setIsConnected,
    setIsTyping,
    enqueueAudio,
    audioQueue,
    isPlayingAudio,
    setIsPlayingAudio,
    audioUnlocked,
    audioVolume,
  } = useChatStore();

  const audioQueueRef = useRef([]);
  const isProcessingAudioRef = useRef(false);
  const lastProcessedMessageRef = useRef(null);

  // WebSocket connection
  const WS_URL = `ws://localhost:8000/ws/chat/${userId}/`;
  
  const { sendJsonMessage, lastJsonMessage, readyState } = useWebSocket(
    WS_URL,
    {
      shouldReconnect: () => true,
      reconnectInterval: 3000,
      reconnectAttempts: 10,
    }
  );

  // Update connection status
  useEffect(() => {
    const connected = readyState === ReadyState.OPEN;
    setIsConnected(connected);
    
    if (connected) {
      console.log('✅ WebSocket connected');
    } else if (readyState === ReadyState.CONNECTING) {
      console.log('🔄 WebSocket connecting...');
    } else if (readyState === ReadyState.CLOSED) {
      console.log('❌ WebSocket closed');
    }
  }, [readyState, setIsConnected]);

  // Process audio queue
  useEffect(() => {
    const processAudioQueue = async () => {
      if (
        audioQueue.length > 0 &&
        !isPlayingAudio &&
        !isProcessingAudioRef.current &&
        audioUnlocked
      ) {
        isProcessingAudioRef.current = true;
        setIsPlayingAudio(true);

        const audioBase64 = audioQueue[0];

        try {
          await playAudioFromBase64(audioBase64, audioVolume);
        } catch (error) {
          console.error('Error playing audio:', error);
        } finally {
          // Remove from queue after playing
          useChatStore.getState().dequeueAudio();
          setIsPlayingAudio(false);
          isProcessingAudioRef.current = false;
        }
      }
    };

    processAudioQueue();
  }, [audioQueue, isPlayingAudio, audioUnlocked, setIsPlayingAudio]);

  // Handle incoming messages
  useEffect(() => {
    if (!lastJsonMessage) return;

    console.log('📩 Received message:', lastJsonMessage);

    const { status, data, message } = lastJsonMessage;

    // Prevent duplicate processing using timestamp + content
    const messageKey = data?.timestamp || lastJsonMessage.timestamp || Date.now();
    if (lastProcessedMessageRef.current === messageKey) {
      console.log('⏭️ Skipping duplicate message');
      return;
    }
    lastProcessedMessageRef.current = messageKey;

    // Handle typing indicator
    if (status === 'typing') {
      setIsTyping(true);
      return;
    }

    setIsTyping(false);

    // Handle connection message
    if (status === 'connected') {
      console.log('✅ Connected:', message);
      return;
    }

    // Handle success response
    if (status === 'success' && data) {
      // Update agent emotion state
      if (data.emotion) {
        setAgentState(data.emotion, data.sulking_level);
      }
      if (data.action === 'volume_updated') {
          console.log('🔊 Volume updated on server:', data.volume);
          return;
      }
      // Add agent message to chat
      addMessage({
        role: 'assistant',
        content: data.vietnamese_display || data.chinese_content,
        chinese_content: data.chinese_content,
        pinyin: data.pinyin,
        emotion: data.emotion,
        action: data.action,
        quiz_list: data.quiz_list || [],
        sulking_level: data.sulking_level,
        correction_detail: data.correction_detail || null,
        audio_base64: data.audio_base64,
      });

      // Queue audio if available
      if (data.audio_base64 && audioUnlocked) {
        enqueueAudio(data.audio_base64);
      }
    }

    // Handle error
    if (status === 'error') {
      console.error('❌ Error from server:', message);
      addMessage({
        role: 'system',
        content: `Lỗi: ${message}`,
      });
    }
  }, [lastJsonMessage, addMessage, setAgentState, setIsTyping, enqueueAudio, audioUnlocked]);

  // Send message function
  const sendMessage = useCallback((text) => {
    if (!text.trim() || readyState !== ReadyState.OPEN) {
      return;
    }

    // Add user message to chat immediately
    addMessage({
      role: 'user',
      content: text,
    });

    // Send to server
    sendJsonMessage({
      action: 'chat',
      message: text,
      user_role: userRole,
    });
  }, [readyState, addMessage, sendJsonMessage, userRole]);
  
  // Reset conversation
  const resetConversation = useCallback(() => {
    sendJsonMessage({
      action: 'reset',
      user_role: userRole,
      
    });
    console.log(userRole),
    useChatStore.getState().clearMessages();
    setAgentState('neutral', 0);
  }, [sendJsonMessage, setAgentState, userRole]);

  // Get current state
  const getUserState = useCallback(() => {
    sendJsonMessage({
      action: 'get_state',
    });
  }, [sendJsonMessage]);

  // Set sulking level (for testing)
  const setSulkingLevel = useCallback((level) => {
    sendJsonMessage({
      action: 'set_sulking',
      level: parseInt(level),
    });
  }, [sendJsonMessage]);

  return {
    sendMessage,
    resetConversation,
    getUserState,
    setSulkingLevel,
    isConnected: readyState === ReadyState.OPEN,
    connectionState: readyState,
  };
  useEffect(() => {

    const timeoutId = setTimeout(() => {
      if (readyState === ReadyState.OPEN) {
        console.log('Sending volume update:', audioVolume);
        sendJsonMessage({
          action: 'set_volume',
          volume: audioVolume,
        });
      }
    }, 500); // Delay 500ms

    // Nếu audioVolume thay đổi trước khi hết 500ms, hủy lệnh gửi cũ đi
    return () => clearTimeout(timeoutId);
  }, [audioVolume, readyState, sendJsonMessage]);
};
  
export default useChat;

