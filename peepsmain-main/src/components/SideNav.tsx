import React, { useEffect, useState, useRef } from 'react';

const navItems = [
  { id: 'about', label: 'About' },
  { id: 'skills', label: 'Skills' },
  { id: 'projects', label: 'Projects' },
  { id: 'education', label: 'Education' },
  { id: 'contact', label: 'Contact' },
];

export function SideNav() {
  const [activeSection, setActiveSection] = useState('about');
  const fillLineRef = useRef<HTMLDivElement>(null);

  // Directly mutate DOM transform to avoid React re-renders during scroll
  useEffect(() => {
    const handleScroll = () => {
      if (!fillLineRef.current) return;
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (totalHeight > 0) {
        const progress = Math.min(1, Math.max(0, window.scrollY / totalHeight));
        fillLineRef.current.style.transform = `scaleY(${progress})`;
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id);
          }
        });
      },
      { threshold: 0.3 }
    );

    navItems.forEach((item) => {
      const el = document.getElementById(item.id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav 
      aria-label="Side navigation"
      className="fixed left-6 top-1/2 -translate-y-1/2 z-[4000] hidden lg:flex flex-col items-center gap-6 select-none"
    >
      {/* Connecting vertical background line */}
      <div className="absolute top-0 bottom-0 left-1/2 -translate-x-1/2 w-[1px] bg-theme-text/10 -z-10" />

      {/* Dynamic Scroll Progress Fill Line (GPU Transform without React re-renders) */}
      <div 
        ref={fillLineRef}
        className="absolute top-0 bottom-0 left-1/2 -translate-x-1/2 w-[1px] bg-theme-text/40 -z-10 origin-top gpu-accelerated"
        style={{ transform: 'scaleY(0)' }}
      />

      {navItems.map((item) => {
        const isActive = activeSection === item.id;
        return (
          <button
            key={item.id}
            onClick={() => scrollToSection(item.id)}
            className="flex flex-col items-center gap-2 group cursor-pointer focus:outline-none interactive py-1"
            aria-label={`Scroll to ${item.label} section`}
          >
            {/* Indicator Dot */}
            <div 
              className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                isActive 
                  ? 'bg-theme-text scale-125 ring-4 ring-theme-text/10' 
                  : 'bg-theme-muted/40 group-hover:bg-theme-text/70'
              }`}
            />

            {/* Vertical Label */}
            <span 
              className={`text-[9px] uppercase tracking-[0.2em] transition-colors duration-300 [writing-mode:vertical-rl] rotate-180 ${
                isActive 
                  ? 'text-theme-text font-medium' 
                  : 'text-theme-muted group-hover:text-theme-text/80'
              }`}
            >
              {item.label}
            </span>
          </button>
        );
      })}
    </nav>
  );
}
