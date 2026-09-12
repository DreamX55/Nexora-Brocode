import React, { useRef, useEffect, useState } from 'react';
import { motion, useScroll, useTransform, AnimatePresence } from 'motion/react';

const cyclingWords = ["Student.", "Developer.", "Builder.", "Creator."];

export function AboutZone() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [imgError, setImgError] = useState(false);
  const [wordIndex, setWordIndex] = useState(0);
  const [avatarMouse, setAvatarMouse] = useState({ x: -200, y: -200 });
  const avatarContainerRef = useRef<HTMLDivElement>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setIsReady(true), 800);
    return () => clearTimeout(timer);
  }, []);

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [60, -60]);
  const opacity = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [0, 1, 1, 0]);

  // Word cycling interval (2.5s per word)
  useEffect(() => {
    const interval = setInterval(() => {
      setWordIndex((prev) => (prev + 1) % cyclingWords.length);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Disable mouse parallax listener on touch screens to save cycles
    if (window.matchMedia('(pointer: coarse)').matches) return;

    const handleMouseMove = (e: MouseEvent) => {
      const { innerWidth, innerHeight } = window;
      const x = (e.clientX / innerWidth - 0.5) * 20;
      const y = (e.clientY / innerHeight - 0.5) * 20;
      setMousePos({ x, y });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const titleWords = "Computer Science".split(" ");

  return (
    <section 
      id="about" 
      ref={containerRef} 
      className="relative min-h-[95vh] sm:min-h-screen flex flex-col items-center justify-between px-4 sm:px-8 md:px-20 pt-[10vh] sm:pt-[12vh] pb-12 overflow-hidden"
    >
      {/* Large Editorial Watermark Text */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none select-none overflow-hidden z-0">
        <span className="font-serif text-[clamp(80px,18vw,200px)] text-theme-text opacity-[0.03] tracking-widest uppercase">
          PORTFOLIO
        </span>
      </div>

      {/* Line Art Decor with Parallax */}
      <motion.svg 
        animate={{ 
          rotate: [-3, 3],
          x: mousePos.x * -1.5,
          y: mousePos.y * -1.5
        }}
        transition={{ 
          rotate: { duration: 5, repeat: Infinity, repeatType: "reverse", ease: "easeInOut" },
          x: { type: "spring", stiffness: 50, damping: 20 },
          y: { type: "spring", stiffness: 50, damping: 20 }
        }}
        className="absolute bottom-16 left-4 sm:bottom-20 sm:left-10 w-36 h-48 sm:w-48 sm:h-64 opacity-20 sm:opacity-30 pointer-events-none origin-bottom gpu-accelerated z-10" 
        viewBox="0 0 100 150" fill="none" stroke="currentColor" strokeWidth="1.5"
      >
        <path d="M50,150 Q45,100 20,80 Q40,90 50,110 Q60,70 80,50 Q65,80 50,90 Q40,40 10,20 Q35,45 50,60" />
      </motion.svg>
      
      <motion.svg 
        animate={{ 
          y: [-10, 10],
          x: mousePos.x * 2,
        }}
        transition={{ 
          y: { duration: 6, repeat: Infinity, repeatType: "reverse", ease: "easeInOut" },
          x: { type: "spring", stiffness: 50, damping: 20 }
        }}
        className="absolute top-20 right-6 sm:top-28 sm:right-20 w-24 h-24 sm:w-32 sm:h-32 opacity-15 sm:opacity-20 pointer-events-none gpu-accelerated z-10" 
        viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="1"
      >
        <circle cx="50" cy="50" r="40" strokeDasharray="4 4" />
        <circle cx="50" cy="50" r="20" />
        <path d="M50,10 L50,90 M10,50 L90,50" strokeWidth="0.5" />
      </motion.svg>

      <motion.div style={{ opacity, y }} className="max-w-4xl text-center relative z-10 w-full flex-grow flex flex-col items-center justify-center">
        
        {/* Profile Photo Component with Local Radial Mask Reveal */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          onMouseMove={(e) => {
            if (!avatarContainerRef.current) return;
            const rect = avatarContainerRef.current.getBoundingClientRect();
            setAvatarMouse({
              x: e.clientX - rect.left,
              y: e.clientY - rect.top
            });
          }}
          onMouseLeave={() => {
            setAvatarMouse({ x: -500, y: -500 });
          }}
          onTouchStart={(e) => {
            if (!avatarContainerRef.current || !e.touches[0]) return;
            const touch = e.touches[0];
            const rect = avatarContainerRef.current.getBoundingClientRect();
            setAvatarMouse({
              x: touch.clientX - rect.left,
              y: touch.clientY - rect.top
            });
          }}
          onTouchMove={(e) => {
            if (!avatarContainerRef.current || !e.touches[0]) return;
            const touch = e.touches[0];
            const rect = avatarContainerRef.current.getBoundingClientRect();
            setAvatarMouse({
              x: touch.clientX - rect.left,
              y: touch.clientY - rect.top
            });
          }}
          onTouchEnd={() => {
            setAvatarMouse({ x: -500, y: -500 });
          }}
          onTouchCancel={() => {
            setAvatarMouse({ x: -500, y: -500 });
          }}
          className="mb-6 sm:mb-8 relative group avatar-hover-zone p-12 sm:p-20 -m-12 sm:-m-20 z-30 touch-none"
        >
          <div 
            ref={avatarContainerRef}
            className="w-40 h-40 sm:w-52 sm:h-52 md:w-60 md:h-60 rounded-full border-2 border-theme-text/20 ring-4 ring-theme-text/20 ring-offset-4 ring-offset-theme-bg overflow-hidden shadow-[0_8px_32px_rgba(61,57,53,0.12)] relative flex items-center justify-center bg-theme-accent transition-all duration-300"
          >
            {!imgError ? (
              <>
                {/* Base Portrait Photo */}
                <img
                  src="/profile1.jpg"
                  alt="Alex Morgan profile portrait"
                  onError={() => setImgError(true)}
                  className="w-full h-full object-cover object-center absolute inset-0"
                />

                {/* Hover Torch Mask Reveal Image */}
                <img
                  src="/profile2.jpg"
                  alt="Alex Morgan creative pose"
                  style={{
                    maskImage: `radial-gradient(circle 150px at ${avatarMouse.x}px ${avatarMouse.y}px, black 0%, black 60%, transparent 70%)`,
                    WebkitMaskImage: `radial-gradient(circle 150px at ${avatarMouse.x}px ${avatarMouse.y}px, black 0%, black 60%, transparent 70%)`,
                    transition: 'mask-image 0.1s ease, -webkit-mask-image 0.1s ease'
                  }}
                  className="w-full h-full object-cover object-center absolute inset-0 z-10 pointer-events-none"
                />
              </>
            ) : (
              <span className="font-serif text-2xl sm:text-3xl text-theme-text font-normal tracking-wide">
                AM
              </span>
            )}
          </div>
        </motion.div>

        {/* Developer Name Label */}
        <motion.p 
          initial={{ opacity: 0, letterSpacing: "0em" }}
          animate={{ opacity: 1, letterSpacing: "0.25em" }}
          transition={{ duration: 1.5, delay: 0.2, ease: "easeOut" }}
          className="text-xs sm:text-sm uppercase tracking-[0.25em] text-theme-muted mb-4 sm:mb-6"
        >
          Alex Morgan
        </motion.p>
        
        <h1 className="text-3xl sm:text-5xl md:text-7xl font-serif leading-tight text-theme-text mb-6 flex flex-col items-center">
          <div className="flex flex-wrap justify-center overflow-hidden">
            {titleWords.map((word, i) => (
              <motion.span
                key={i}
                initial={{ y: "100%" }}
                animate={{ y: 0 }}
                transition={{ duration: 0.8, delay: 0.3 + i * 0.1, ease: [0.33, 1, 0.68, 1] }}
                className="mr-2 sm:mr-4 last:mr-0 inline-block"
              >
                {word}
              </motion.span>
            ))}
          </div>
          <div className="flex flex-wrap justify-center items-center italic text-theme-muted">
            <span className="mr-2 sm:mr-3 inline-block">Engineering</span>
            {/* Dynamic Cycling Word with AnimatePresence */}
            <span className="inline-block relative min-w-[120px] text-left">
              <AnimatePresence mode="wait">
                <motion.span
                  key={cyclingWords[wordIndex]}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.5, ease: "easeInOut" }}
                  className="inline-block text-theme-text font-medium"
                >
                  {cyclingWords[wordIndex]}
                </motion.span>
              </AnimatePresence>
            </span>
          </div>
        </h1>
        
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.9 }}
          className="text-base sm:text-lg md:text-xl text-theme-text max-w-2xl mx-auto mt-4 sm:mt-6 font-light px-2 leading-relaxed"
        >
          Architecting intelligent systems and crafting immersive digital experiences at the intersection of <span className="font-medium italic">AI, Design, and Engineering</span>.
        </motion.p>

        {/* Hero Stats Row */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1.2 }}
          className="flex flex-wrap items-center justify-center gap-4 sm:gap-8 mt-8 sm:mt-10 text-xs uppercase tracking-widest text-theme-muted"
        >
          <span>4+ Projects</span>
          <span className="w-[1px] h-3 bg-theme-text/20" />
          <span>4 Languages</span>
          <span className="w-[1px] h-3 bg-theme-text/20" />
          <span>Available 2025</span>
        </motion.div>
      </motion.div>

      {/* Animated Scroll Indicator */}
      <motion.div 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 1.4 }}
        className="flex flex-col items-center gap-2 mt-8 z-10 select-none"
      >
        <div className="w-[1px] h-10 bg-theme-text/15 relative overflow-hidden">
          <motion.div 
            className="w-full h-3 bg-theme-text rounded-full absolute top-0 left-0"
            animate={{ y: [0, 40] }}
            transition={{ duration: 1.8, repeat: Infinity, ease: "easeInOut" }}
          />
        </div>
        <span className="text-[9px] uppercase tracking-[0.3em] text-theme-muted font-sans">
          Scroll
        </span>
      </motion.div>
    </section>
  );
}
