import React, { useState, useEffect } from 'react';
import { motion, useAnimation, useMotionValue } from 'motion/react';

interface EntrySequenceProps {
  onEnter: () => void;
  key?: React.Key;
}

export function EntrySequence({ onEnter }: EntrySequenceProps) {
  const [typingComplete, setTypingComplete] = useState(false);
  const text = "Alex Morgan";
  const [displayedText, setDisplayedText] = useState("");

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setDisplayedText(text.slice(0, i + 1));
      i++;
      if (i === text.length) {
        clearInterval(interval);
        setTimeout(() => setTypingComplete(true), 600);
      }
    }, 90); // typing speed

    return () => clearInterval(interval);
  }, []);

  // Keyboard shortcut listener (Enter key triggers entry)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Enter') {
        onEnter();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onEnter]);

  return (
    <motion.div 
      className="fixed inset-0 z-[5000] flex flex-col items-center justify-center bg-theme-loader px-4 overflow-hidden"
      initial={{ y: 0 }}
      exit={{ y: '-100%' }}
      transition={{ duration: 1, ease: [0.76, 0, 0.24, 1] }}
    >
      <div className="relative z-10 text-center font-serif text-3xl sm:text-4xl md:text-5xl text-theme-text select-none">
        <span>{displayedText}</span>
        <motion.span
          animate={{ opacity: [1, 0] }}
          transition={{ repeat: Infinity, duration: 0.8, ease: "linear" }}
          className="inline-block ml-1"
        >
          |
        </motion.span>
      </div>

      {typingComplete && (
        <Lamp onPull={onEnter} />
      )}
    </motion.div>
  );
}

function Lamp({ onPull }: { onPull: () => void }) {
  const y = useMotionValue(0);
  const controls = useAnimation();
  
  const handleDragEnd = (_event: any, info: any) => {
    if (info.offset.y > 80 || info.velocity.y > 300) {
      onPull();
    } else {
      controls.start({ y: 0, transition: { type: "spring", bounce: 0.6 } });
    }
  };

  useEffect(() => {
    controls.start({ y: 0, transition: { type: "spring", damping: 12, stiffness: 50 } });
  }, [controls]);

  return (
    <motion.div 
      className="absolute top-[-300px] sm:top-[-340px] left-1/2 -translate-x-1/2 flex flex-col items-center cursor-grab active:cursor-grabbing z-[5200] interactive touch-none gpu-accelerated"
      initial={{ y: -100 }}
      animate={controls}
      drag="y"
      dragConstraints={{ top: 0, bottom: 160 }}
      dragElastic={0.3}
      onDragEnd={handleDragEnd}
      style={{ y, willChange: 'transform' }}
      role="button"
      tabIndex={0}
      aria-label="Pull lamp cord to enter site"
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          onPull();
        }
      }}
    >
      <motion.div
        animate={{ rotate: [-1.5, 1.5] }}
        transition={{ repeat: Infinity, duration: 2, ease: "easeInOut", repeatType: "reverse" }}
        style={{ transformOrigin: "top center" }}
        className="relative flex flex-col items-center"
      >
        <svg width="120" height="420" viewBox="0 0 120 420" className="w-[100px] sm:w-[120px]">
          <line x1="60" y1="0" x2="60" y2="300" stroke="#3D3935" strokeWidth="2"/>
          <path d="M20,300 Q60,240 100,300 Z" fill="#8A8273"/>
          <circle cx="60" cy="300" r="15" fill="#FFFBEB"/>
          <line x1="60" y1="315" x2="60" y2="385" stroke="#3D3935" strokeWidth="1.5" strokeDasharray="3 2"/>
          
          {/* Pulsating pulse ring growing directly from the center of the cord handle circle (60, 390) */}
          <motion.circle 
            cx="60" 
            cy="390" 
            r="8" 
            fill="none" 
            stroke="#3D3935" 
            strokeWidth="1.5"
            animate={{ r: [8, 20, 8], opacity: [0.7, 0, 0.7] }}
            transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut" }}
          />

          {/* Animated cord handle ball */}
          <circle cx="60" cy="390" r="8" fill="#3D3935" />
        </svg>

        <p className="absolute bottom-[-36px] left-1/2 -translate-x-1/2 text-[9px] sm:text-[10px] uppercase tracking-[0.3em] opacity-50 whitespace-nowrap text-theme-text font-sans select-none">
          Pull cord ↓
        </p>
      </motion.div>
    </motion.div>
  );
}
