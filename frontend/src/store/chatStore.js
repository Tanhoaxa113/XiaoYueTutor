import { create } from 'zustand';

/**
 * Global chat state management using Zustand
 */
const useChatStore = create((set) => ({
  // User state
  userId: 'user_' + Math.random().toString(36).substr(2, 9),
  userRole: 'Sư huynh', // Default: Senior Brother
  
  // Agent state
  agentRole: 'Muội muội', // Little Junior Sister
  agentEmotion: 'neutral',
  sulkingLevel: 0,
  
  // Messages
  messages: [],
  
  // Audio state
  audioQueue: [],
  isPlayingAudio: false,
  audioUnlocked: false,
  audioVolume: 0.7,

  // UI state
  isConnected: false,
  isTyping: false,
  selectedCharacter: null,
  showHanziModal: false,
  
  // Actions
  setUserRole: (role) => set({ userRole: role }),
  setAudioUnlocked: (unlocked) => set({ audioUnlocked: unlocked }),
  setAgentState: (emotion, sulkingLevel) => set({ 
    agentEmotion: emotion || 'neutral',
    sulkingLevel: sulkingLevel || 0,
  }),
  
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, {
      id: Date.now() + Math.random(),
      timestamp: new Date().toISOString(),
      ...message,
    }],
  })),
  
  clearMessages: () => set({ messages: [] }),
  
  setIsConnected: (connected) => set({ isConnected: connected }),
  setAudioVolume: (volume) => set({ audioVolume: volume }),
  setIsTyping: (typing) => set({ isTyping: typing }),
  
  // Audio queue management
  enqueueAudio: (audioBase64) => set((state) => ({
    audioQueue: [...state.audioQueue, audioBase64],
  })),
  
  dequeueAudio: () => set((state) => ({
    audioQueue: state.audioQueue.slice(1),
  })),
  
  setIsPlayingAudio: (isPlaying) => set({ isPlayingAudio: isPlaying }),
  
  // Hanzi modal
  openHanziModal: (character) => set({ 
    selectedCharacter: character,
    showHanziModal: true,
  }),
  
  closeHanziModal: () => set({ 
    showHanziModal: false,
    selectedCharacter: null,
  }),
}));

export default useChatStore;

