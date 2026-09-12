import React, { useRef, useState } from 'react';
import { motion, useScroll, useTransform } from 'motion/react';

const skillCategories = [
  {
    title: "Programming Languages",
    skills: ["C", "C++", "Python", "Java"],
    colSpan: "md:col-span-8",
    rowSpan: "md:row-span-1",
    svg: (
      <svg className="absolute right-0 bottom-0 w-48 h-48 sm:w-64 sm:h-64 opacity-10 text-theme-text pointer-events-none" viewBox="0 0 200 200" fill="none" stroke="currentColor" strokeWidth="1">
        <path d="M10,100 Q50,10 100,100 T190,100" />
        <path d="M10,120 Q50,30 100,120 T190,120" />
        <path d="M10,140 Q50,50 100,140 T190,140" />
      </svg>
    )
  },
  {
    title: "Web Development",
    skills: ["HTML", "CSS", "JavaScript"],
    colSpan: "md:col-span-4",
    rowSpan: "md:row-span-2",
    svg: (
      <svg className="absolute -left-10 -bottom-10 w-48 h-48 sm:w-64 sm:h-64 opacity-10 text-theme-text pointer-events-none" viewBox="0 0 200 200" fill="none" stroke="currentColor" strokeWidth="1">
        <path d="M100,200 Q100,100 50,50" />
        <path d="M100,150 Q150,120 180,80" />
        <path d="M100,100 Q120,50 100,10" />
        <circle cx="50" cy="50" r="5" />
        <circle cx="180" cy="80" r="5" />
        <circle cx="100" cy="10" r="5" />
      </svg>
    )
  },
  {
    title: "Tools & Workflow",
    skills: ["Git", "VS Code"],
    colSpan: "md:col-span-8",
    rowSpan: "md:row-span-1",
    svg: (
      <svg className="absolute right-10 top-10 w-36 h-36 sm:w-48 sm:h-48 opacity-10 text-theme-text pointer-events-none" viewBox="0 0 200 200" fill="none" stroke="currentColor" strokeWidth="1">
        <rect x="40" y="40" width="120" height="120" transform="rotate(45 100 100)" />
        <rect x="60" y="60" width="80" height="80" transform="rotate(45 100 100)" />
      </svg>
    )
  }
];

interface GlowCardProps {
  children: React.ReactNode;
  className: string;
  delay: number;
  key?: React.Key;
}

function GlowCard({ children, className, delay }: GlowCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [mousePos, setMousePos] = useState({ x: -1000, y: -1000 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current || window.matchMedia('(pointer: coarse)').matches) return;
    const rect = cardRef.current.getBoundingClientRect();
    setMousePos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  const handleMouseLeave = () => {
    setMousePos({ x: -1000, y: -1000 });
  };

  return (
    <motion.div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8, delay }}
      className={`relative overflow-hidden bg-theme-text/5 border border-theme-text/10 p-6 sm:p-8 flex flex-col justify-between group interactive rounded-xl ${className}`}
    >
      <div
        className="pointer-events-none absolute -inset-px opacity-0 transition duration-300 group-hover:opacity-100 hidden md:block"
        style={{
          background: `radial-gradient(600px circle at ${mousePos.x}px ${mousePos.y}px, rgba(255,255,255,0.06), transparent 40%)`,
        }}
      />
      {children}
    </motion.div>
  );
}

export function SkillsZone() {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [40, -40]);

  return (
    <section id="skills" ref={containerRef} className="relative flex flex-col justify-center px-4 sm:px-6 py-16 sm:py-20">
      <div className="max-w-6xl mx-auto w-full">
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-[10px] uppercase tracking-[0.4em] text-theme-muted mb-8 sm:mb-12"
        >
          Technical Arsenal
        </motion.p>

        <motion.div style={{ y }} className="grid grid-cols-1 md:grid-cols-12 gap-4 sm:gap-6 auto-rows-[minmax(160px,auto)]">
          {skillCategories.map((category, idx) => (
            <GlowCard 
              key={category.title}
              delay={idx * 0.15}
              className={`${category.colSpan} ${category.rowSpan}`}
            >
              <motion.div 
                className="absolute inset-0 pointer-events-none gpu-accelerated"
                animate={{ y: [0, -8, 0] }}
                transition={{ duration: 5 + idx, repeat: Infinity, ease: "easeInOut" }}
              >
                {category.svg}
              </motion.div>
              
              <div className="relative z-10">
                <h3 className="text-xl sm:text-2xl font-serif text-theme-text mb-4 sm:mb-6">{category.title}</h3>
                <div className="flex flex-wrap gap-2.5 sm:gap-3">
                  {category.skills.map((skill, sIdx) => (
                    <motion.span 
                      key={skill} 
                      initial={{ opacity: 0, scale: 0.8 }}
                      whileInView={{ opacity: 1, scale: 1 }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.4, delay: idx * 0.15 + sIdx * 0.05 + 0.3 }}
                      whileHover={{ scale: 1.05 }}
                      className="px-3.5 sm:px-4 py-1.5 sm:py-2 bg-theme-bg/80 backdrop-blur-sm border border-theme-text/20 text-xs sm:text-sm text-theme-text rounded-full transition-all duration-300 hover:shadow-[inset_0_0_12px_rgba(61,57,53,0.08)] hover:border-theme-text/40"
                    >
                      {skill}
                    </motion.span>
                  ))}
                </div>
              </div>
            </GlowCard>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
