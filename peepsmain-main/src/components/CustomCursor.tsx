import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'motion/react';

interface CustomCursorProps {
  hasEntered: boolean;
}

export function CustomCursor({ hasEntered }: CustomCursorProps) {
  const [pos, setPos] = useState({ x: -100, y: -100 });
  const [isHovering, setIsHovering] = useState(false);
  const [isOverAvatar, setIsOverAvatar] = useState(false);
  const [isTouchDevice, setIsTouchDevice] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  // Ref gate: prevents any mousemove from showing cursor during entry transition.
  // Locked to false when hasEntered fires, unlocked after 1400ms.
  const allowVisibilityRef = useRef(true);
  const lockTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // React prop-based entry detection — guaranteed to run before any DOM events
  // from the newly-mounted MainCanvas reach the cursor handlers.
  useEffect(() => {
    if (!hasEntered) return;
    allowVisibilityRef.current = false;
    setIsVisible(false);
    setIsHovering(false);
    setIsOverAvatar(false);
    setPos({ x: -100, y: -100 });
    if (lockTimerRef.current) clearTimeout(lockTimerRef.current);
    lockTimerRef.current = setTimeout(() => {
      allowVisibilityRef.current = true;
    }, 1400);
  }, [hasEntered]);

  useEffect(() => {
    if (window.matchMedia('(pointer: coarse)').matches) {
      setIsTouchDevice(true);
      return;
    }

    const move = (e: MouseEvent) => {
      setPos({ x: e.clientX, y: e.clientY });
      if (allowVisibilityRef.current) {
        setIsVisible(true);
      }
      const target = e.target as HTMLElement | null;
      
      // Direct DOM target check for avatar zone
      const overAvatar = !!(target && target.closest('.avatar-hover-zone'));
      setIsOverAvatar(overAvatar);

      if (target && target.closest('a, button, .interactive, input, textarea')) {
        setIsHovering(true);
      } else {
        setIsHovering(false);
      }
    };
    window.addEventListener('mousemove', move);

    return () => {
      window.removeEventListener('mousemove', move);
      if (lockTimerRef.current) clearTimeout(lockTimerRef.current);
    };
  }, []);

  if (isTouchDevice) return null;

  return (
    <motion.div
      className="fixed top-0 left-0 rounded-full pointer-events-none z-[10000] hidden md:block gpu-accelerated"
      initial={{ opacity: 0, width: 0, height: 0 }}
      animate={{
        x: pos.x - (isOverAvatar || isHovering ? 40 : 10),
        y: pos.y - (isOverAvatar || isHovering ? 40 : 10),
        width: isVisible ? (isOverAvatar || isHovering ? 80 : 20) : 0,
        height: isVisible ? (isOverAvatar || isHovering ? 80 : 20) : 0,
        backgroundColor: isOverAvatar ? 'transparent' : (isHovering ? '#F5F2EB' : '#8A8273'),
        opacity: isVisible ? (isOverAvatar ? 0 : (isHovering ? 1 : 0.5)) : 0,
        mixBlendMode: isOverAvatar ? 'normal' : (isHovering ? 'difference' : 'normal')
      }}
      transition={{ type: "tween", ease: "backOut", duration: 0.15 }}
      style={{ willChange: 'transform, width, height' }}
    />
  );
}
