/**
 * Audio playback utilities
 */

let audioContext = null;

/**
 * Initialize AudioContext (must be called on user interaction)
 */
export const initAudioContext = () => {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContext;
};

/**
 * Convert Base64 string to audio and play it
 * @param {string} base64Audio - Base64 encoded audio (MP3)
 * @returns {Promise<void>}
 */
export const playAudioFromBase64 = async (base64Audio, volume = 1.0) => {
  if (!base64Audio) {
    throw new Error('No audio data provided');
  }

  try {
    // Ensure AudioContext is initialized
    if (!audioContext) {
      audioContext = initAudioContext();
    }

    // Resume context if suspended (browser autoplay policy)
    if (audioContext.state === 'suspended') {
      await audioContext.resume();
    }

    // Convert base64 to binary
    const binaryString = atob(base64Audio);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    // Create audio element (simpler approach for MP3)
    return new Promise((resolve, reject) => {
      const audio = new Audio();
      const blob = new Blob([bytes], { type: 'audio/mpeg' });
      const url = URL.createObjectURL(blob);

      audio.src = url;
      audio.volume = volume;

      audio.onended = () => {
        URL.revokeObjectURL(url);
        resolve();
      };

      audio.onerror = (error) => {
        URL.revokeObjectURL(url);
        reject(error);
      };

      audio.play().catch(reject);
    });
  } catch (error) {
    console.error('Error playing audio:', error);
    throw error;
  }
};

/**
 * Preload audio from base64 (for smoother playback)
 * @param {string} base64Audio
 * @returns {Promise<HTMLAudioElement>}
 */
export const preloadAudio = async (base64Audio) => {
  const binaryString = atob(base64Audio);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }

  const blob = new Blob([bytes], { type: 'audio/mpeg' });
  const url = URL.createObjectURL(blob);
  const audio = new Audio(url);

  return new Promise((resolve, reject) => {
    audio.oncanplaythrough = () => resolve(audio);
    audio.onerror = reject;
    audio.load();
  });
};

