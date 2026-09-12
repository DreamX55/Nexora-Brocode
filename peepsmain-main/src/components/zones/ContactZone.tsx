import React, { useRef, useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Github, Linkedin, Twitter, Mail } from 'lucide-react';

const interests = [
  "Web Development",
  "UI/UX Design",
  "Artificial Intelligence",
  "Creative Coding"
];

function Magnetic({ children }: { children: React.ReactElement }) {
  const ref = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isTouch, setIsTouch] = useState(false);

  useEffect(() => {
    if (window.matchMedia('(pointer: coarse)').matches) {
      setIsTouch(true);
    }
  }, []);

  const handleMouse = (e: React.MouseEvent<HTMLDivElement>) => {
    if (isTouch) return;
    const { clientX, clientY } = e;
    const { height, width, left, top } = ref.current!.getBoundingClientRect();
    const middleX = clientX - (left + width / 2);
    const middleY = clientY - (top + height / 2);
    setPosition({ x: middleX * 0.2, y: middleY * 0.2 });
  };

  const reset = () => {
    setPosition({ x: 0, y: 0 });
  };

  if (isTouch) {
    return <div ref={ref}>{children}</div>;
  }

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMouse}
      onMouseLeave={reset}
      animate={{ x: position.x, y: position.y }}
      transition={{ type: "spring", stiffness: 150, damping: 15, mass: 0.1 }}
    >
      {children}
    </motion.div>
  );
}

export function ContactZone() {
  return (
    <section id="contact" className="relative min-h-screen bg-theme-bg flex flex-col justify-between overflow-hidden">
      
      {/* Interests Section */}
      <div className="w-full flex flex-col items-center justify-center pt-20 sm:pt-32 pb-10 sm:pb-12 px-4 sm:px-5">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-10 sm:mb-16"
        >
          <p className="text-xs sm:text-sm tracking-[0.3em] uppercase text-theme-muted mb-3 sm:mb-4">Current Fascinations</p>
          <h2 className="text-4xl sm:text-5xl font-serif italic text-theme-text">Core Interests.</h2>
        </motion.div>
        
        <div className="flex flex-wrap justify-center gap-3 sm:gap-4 md:gap-6 max-w-4xl mx-auto relative z-20 px-2">
          {interests.map((interest, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="px-5 sm:px-8 py-3 sm:py-4 rounded-full border border-theme-text/20 font-serif italic text-base sm:text-xl md:text-2xl text-theme-text bg-theme-bg/50 backdrop-blur-sm interactive hover:bg-theme-text hover:text-theme-bg hover:border-theme-text transition-all duration-500 cursor-default"
            >
              {interest}
            </motion.div>
          ))}
        </div>
      </div>

      {/* Contact Section */}
      <div className="flex-grow flex flex-col items-center justify-center bg-[#1a1918] text-[#D4CFC4] py-16 sm:py-24 px-4 sm:px-5 rounded-t-[2.5rem] md:rounded-t-[5rem] mt-8 sm:mt-10 relative z-30 min-h-[440px]">
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto w-full"
        >
          <p className="font-serif text-3xl sm:text-5xl md:text-7xl italic mb-4 sm:mb-6 text-white px-2">
            Let's build the future.
          </p>
          
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xs sm:text-sm tracking-widest uppercase text-[#8A8273] mb-12 px-2"
          >
            Open to freelance, collaboration & full-time roles.
          </motion.p>
          
          {/* Horizontal Rule above social links */}
          <div className="border-t border-[#8A8273]/20 pt-8 sm:pt-12 w-full max-w-xl mx-auto">
            <div className="flex flex-wrap justify-center gap-4 sm:gap-6 md:gap-12 px-2">
              <ContactLink 
                href="mailto:hello@alexmorgan.dev" 
                icon={<Mail />} 
                label="Email" 
                ariaLabel="Send email to Alex Morgan" 
                tooltip="hello@alexmorgan.dev"
              />
              <ContactLink href="https://github.com" icon={<Github />} label="GitHub" ariaLabel="Visit GitHub profile" />
              <ContactLink href="https://linkedin.com" icon={<Linkedin />} label="LinkedIn" ariaLabel="Visit LinkedIn profile" />
              <ContactLink href="https://twitter.com" icon={<Twitter />} label="Twitter" ariaLabel="Visit Twitter profile" />
            </div>
          </div>
        </motion.div>

        {/* Footer */}
        <div className="mt-16 sm:absolute sm:bottom-10 w-full text-center">
          <p className="text-[10px] uppercase tracking-widest text-[#8A8273]">
            © {new Date().getFullYear()} Alex Morgan
          </p>
        </div>
      </div>
    </section>
  );
}

function ContactLink({ href, icon, label, ariaLabel, tooltip }: { href: string, icon: React.ReactNode, label: string, ariaLabel: string, tooltip?: string }) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <Magnetic>
      <div 
        className="relative flex flex-col items-center"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Tooltip on Hover */}
        <AnimatePresence>
          {tooltip && isHovered && (
            <motion.div
              initial={{ opacity: 0, y: 4, scale: 0.95 }}
              animate={{ opacity: 1, y: -8, scale: 1 }}
              exit={{ opacity: 0, y: 4, scale: 0.95 }}
              transition={{ duration: 0.2 }}
              className="absolute -top-10 z-50 bg-[#3D3935] text-[#F5F2EB] text-[10px] font-mono px-2.5 py-1 rounded shadow-lg whitespace-nowrap pointer-events-none border border-[#8A8273]/30"
            >
              {tooltip}
            </motion.div>
          )}
        </AnimatePresence>

        <a 
          href={href} 
          target="_blank" 
          rel="noopener noreferrer"
          aria-label={ariaLabel}
          className="flex flex-col items-center gap-2.5 sm:gap-3 text-[#8A8273] hover:text-white transition-colors duration-300 interactive group p-2 min-w-[64px] min-h-[64px] justify-center focus:outline-none focus:ring-2 focus:ring-white/40 rounded-xl"
        >
          <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-full border border-[#8A8273]/30 flex items-center justify-center group-hover:border-white transition-colors duration-300">
            {icon}
          </div>
          <span className="text-[10px] sm:text-xs tracking-widest uppercase">{label}</span>
        </a>
      </div>
    </Magnetic>
  );
}
