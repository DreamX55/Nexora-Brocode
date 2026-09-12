import { useEffect, useState, useRef } from 'react';
import Lenis from 'lenis';
import { AnimatePresence, motion } from 'motion/react';
import { NoiseOverlay } from './components/NoiseOverlay';
import { EntrySequence } from './components/EntrySequence';
import { MainCanvas } from './components/MainCanvas';
import { CustomCursor } from './components/CustomCursor';
import { SideNav } from './components/SideNav';
import { BackToTop } from './components/BackToTop';

export default function App() {
  const [hasEntered, setHasEntered] = useState(false);
  const [showShutter, setShowShutter] = useState(false);
  const lenisRef = useRef<Lenis | null>(null);

  // Initialize Lenis once on mount
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 2,
    });

    lenisRef.current = lenis;

    let rafId: number;
    function raf(time: number) {
      lenis.raf(time);
      rafId = requestAnimationFrame(raf);
    }

    rafId = requestAnimationFrame(raf);

    // Initial stop if not entered
    lenis.stop();

    return () => {
      cancelAnimationFrame(rafId);
      lenis.destroy();
      lenisRef.current = null;
    };
  }, []);

  // Control Lenis scroll start/stop cleanly based on entry state
  useEffect(() => {
    if (!lenisRef.current) return;
    if (hasEntered) {
      lenisRef.current.start();
    } else {
      lenisRef.current.stop();
    }
  }, [hasEntered]);

  const handleEnter = () => {
    setHasEntered(true);
    setShowShutter(true);
    setTimeout(() => setShowShutter(false), 350);
  };

  return (
    <div className="relative w-full min-h-screen bg-theme-bg">
      <NoiseOverlay />
      <CustomCursor hasEntered={hasEntered} />
      
      {/* Light switch / camera shutter transition flash */}
      {showShutter && (
        <motion.div 
          initial={{ opacity: 1 }}
          animate={{ opacity: 0 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          className="fixed inset-0 z-[6000] bg-theme-bg pointer-events-none"
        />
      )}

      <AnimatePresence mode="wait">
        {!hasEntered && (
          <EntrySequence key="entry-sequence" onEnter={handleEnter} />
        )}
      </AnimatePresence>
      
      {hasEntered && (
        <>
          <SideNav />
          <MainCanvas />
          <BackToTop />
        </>
      )}
    </div>
  );
}
