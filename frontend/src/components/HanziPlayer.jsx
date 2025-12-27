import { useEffect, useRef } from 'react';
import HanziWriter from 'hanzi-writer';

/**
 * HanziPlayer component - Animates Chinese character stroke order
 * 
 * @param {Object} props
 * @param {string} props.character - Chinese character to display
 * @param {number} props.size - Size of the character canvas (default: 200)
 * @param {boolean} props.autoAnimate - Auto-play animation on mount (default: true)
 * @param {Function} props.onComplete - Callback when animation completes
 */
const HanziPlayer = ({ 
  character, 
  size = 200, 
  autoAnimate = true,
  onComplete,
}) => {
  const containerRef = useRef(null);
  const writerRef = useRef(null);

  useEffect(() => {
    if (!character || !containerRef.current) return;

    // Clear previous content
    containerRef.current.innerHTML = '';

    try {
      // Create HanziWriter instance
      const writer = HanziWriter.create(containerRef.current, character, {
        width: size,
        height: size,
        padding: 10,
        strokeColor: '#1c1917', // Ink black
        outlineColor: '#d6d3d1', // Stone-300
        radicalColor: '#dc2626', // Cinnabar red
        showOutline: true,
        showCharacter: false, // Start hidden for animation
        strokeAnimationSpeed: 2,
        delayBetweenStrokes: 100,
      });

      writerRef.current = writer;

      // Auto-animate if enabled
      if (autoAnimate) {
        writer.animateCharacter({
          onComplete: () => {
            if (onComplete) onComplete();
          },
        });
      }
    } catch (error) {
      console.error('Error creating HanziWriter:', error);
      // Fallback: show character as text
      containerRef.current.innerHTML = `
        <div class="flex items-center justify-center" style="width: ${size}px; height: ${size}px;">
          <span class="text-6xl font-chinese text-ink-900">${character}</span>
        </div>
      `;
    }

    // Cleanup
    return () => {
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
      }
    };
  }, [character, size, autoAnimate, onComplete]);

  // Control functions
  const animate = () => {
    if (writerRef.current) {
      writerRef.current.animateCharacter();
    }
  };

  const showCharacter = () => {
    if (writerRef.current) {
      writerRef.current.showCharacter();
    }
  };

  const hideCharacter = () => {
    if (writerRef.current) {
      writerRef.current.hideCharacter();
    }
  };

  const quiz = () => {
    if (writerRef.current) {
      writerRef.current.quiz({
        onMistake: (strokeData) => {
          console.log('Mistake on stroke:', strokeData);
        },
        onCorrectStroke: (strokeData) => {
          console.log('Correct stroke:', strokeData);
        },
        onComplete: (summaryData) => {
          console.log('Quiz complete:', summaryData);
          if (onComplete) onComplete();
        },
      });
    }
  };

  return (
    <div className="flex flex-col items-center space-y-4">
      {/* Character canvas */}
      <div 
        ref={containerRef}
        className="bg-parchment-50 border-2 border-stone-300 rounded-lg shadow-scroll"
      />
      
      {/* Controls */}
      <div className="flex gap-2 flex-wrap justify-center">
        <button
          onClick={animate}
          className="px-4 py-2 bg-stone-700 text-white rounded-md hover:bg-stone-800 transition-colors text-sm font-serif"
        >
          🎬 Xem lại
        </button>
        
        <button
          onClick={showCharacter}
          className="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 transition-colors text-sm font-serif"
        >
          👁️ Hiện
        </button>
        
        <button
          onClick={hideCharacter}
          className="px-4 py-2 bg-stone-400 text-white rounded-md hover:bg-stone-500 transition-colors text-sm font-serif"
        >
          🙈 Ẩn
        </button>
        
        <button
          onClick={quiz}
          className="px-4 py-2 bg-cinnabar-700 text-white rounded-md hover:bg-cinnabar-800 transition-colors text-sm font-serif"
        >
          ✍️ Luyện viết
        </button>
      </div>
    </div>
  );
};

export default HanziPlayer;

