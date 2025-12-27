/**
 * Helper functions for emotion display and mapping
 */

/**
 * Emotion to emoji mapping
 */
export const EMOTION_EMOJIS = {
  neutral: '😊',
  happy: '😄',
  excited: '🤩',
  cheerful: '😁',
  strict: '😠',
  concerned: '😟',
  sulking: '😤',
  angry: '😡',
};

/**
 * Emotion to Vietnamese text
 */
export const EMOTION_TEXT_VI = {
  neutral: 'Bình thường',
  happy: 'Vui vẻ',
  excited: 'Phấn khích',
  cheerful: 'Vui tươi',
  strict: 'Nghiêm khắc',
  concerned: 'Lo lắng',
  sulking: 'Đang dỗi',
  angry: 'Giận dữ',
};

/**
 * Emotion to color classes
 */
export const EMOTION_COLORS = {
  neutral: 'text-stone-600',
  happy: 'text-yellow-600',
  excited: 'text-orange-600',
  cheerful: 'text-green-600',
  strict: 'text-red-700',
  concerned: 'text-amber-700',
  sulking: 'text-purple-600',
  angry: 'text-red-800',
};

/**
 * Get emotion display info
 */
export const getEmotionDisplay = (emotion) => {
  return {
    emoji: EMOTION_EMOJIS[emotion] || EMOTION_EMOJIS.neutral,
    text: EMOTION_TEXT_VI[emotion] || EMOTION_TEXT_VI.neutral,
    color: EMOTION_COLORS[emotion] || EMOTION_COLORS.neutral,
  };
};

/**
 * Sulking level to text
 */
export const SULKING_LEVELS = {
  0: 'Vui vẻ',
  1: 'Hơi dỗi',
  2: 'Đang dỗi',
  3: 'Rất giận',
};

/**
 * Get sulking level description
 */
export const getSulkingDescription = (level) => {
  return SULKING_LEVELS[level] || SULKING_LEVELS[0];
};

