import React, { useRef } from 'react';
import { motion, useScroll, useTransform } from 'motion/react';
import { Award, BookOpen } from 'lucide-react';

export function EducationZone() {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start center", "end center"]
  });

  const scaleY = useTransform(scrollYProgress, [0, 1], [0, 1]);

  return (
    <section id="education" ref={containerRef} className="relative bg-[#EAE6DD] py-16 sm:py-20 px-4 sm:px-6 overflow-hidden">
      
      {/* Journey & Milestones */}
      <div className="max-w-4xl w-full mx-auto relative z-10 mb-20 sm:mb-32">
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center text-xs sm:text-sm tracking-[0.3em] uppercase text-theme-muted mb-12 sm:mb-16"
        >
          Journey & Milestones
        </motion.p>
        
        <div className="relative max-w-3xl mx-auto">
          {/* Timeline Line */}
          <div className="absolute left-[11px] sm:left-[23px] top-0 bottom-0 w-[1px] bg-theme-muted/30" />
          <motion.div 
            className="absolute left-[11px] sm:left-[23px] top-0 w-[2px] bg-theme-text origin-top gpu-accelerated" 
            style={{ scaleY, height: '100%' }} 
          />
          
          <div className="space-y-16 sm:space-y-24">
            <TimelineItem 
              glyph="✦"
              time="Current"
              title="B.Tech in Computer Science"
              desc="Focusing on modern architectures, algorithms, and application development."
              isActive={true}
            />
            <TimelineItem 
              glyph="◆"
              time="Pre-University"
              title="Pinecrest Academy"
              subtitle="Advanced Sciences — 4.0 GPA"
              desc="Deep focus on advanced mathematics, physics, and computer science fundamentals."
            />
            <TimelineItem 
              glyph="◆"
              time="Foundation"
              title="Oakridge High School"
              subtitle="Secondary Education"
              desc="Cultivated early interest in logical problem solving, web technologies, and coding."
            />
          </div>
        </div>
      </div>

      {/* Certifications */}
      <div className="max-w-4xl mx-auto relative z-10">
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center text-xs sm:text-sm tracking-[0.3em] uppercase text-theme-muted mb-12 sm:mb-16"
        >
          Certifications & Achievements
        </motion.p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
          <CertCard 
            icon={<BookOpen className="w-5 h-5" />}
            title="Machine Learning Specialization"
            issuer="Coursera & Stanford"
            desc="Advanced neural network design and predictive modeling."
          />
          <CertCard 
            icon={<Award className="w-5 h-5" />}
            title="Frontend Excellence"
            issuer="Creative Coding Institute"
            desc="Mastery of creative coding, WebGL, and high-performance UI orchestration."
          />
        </div>
      </div>

      {/* Line Art Plant Background */}
      <motion.svg 
        animate={{ rotate: [-2, 2] }}
        transition={{ duration: 6, repeat: Infinity, repeatType: "reverse", ease: "easeInOut" }}
        className="absolute top-1/4 -left-10 w-48 h-72 sm:w-64 sm:h-96 opacity-10 pointer-events-none origin-bottom gpu-accelerated" 
        viewBox="0 0 100 200" fill="none" stroke="currentColor" strokeWidth="2"
      >
        <path d="M50,200 Q60,100 20,50 Q60,80 50,20 Q80,80 90,40" strokeLinecap="round" />
      </motion.svg>
    </section>
  );
}

function TimelineItem({ glyph, time, title, subtitle, desc, isActive }: any) {
  return (
    <motion.div 
      initial={{ opacity: 0, x: -20 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.8 }}
      className="relative pl-10 sm:pl-20 group interactive"
    >
      {/* Dot */}
      <div className={`absolute left-[7px] sm:left-[19px] top-[6px] w-[10px] h-[10px] rounded-full border-2 border-theme-text transition-all duration-300 group-hover:scale-150 group-hover:bg-theme-text z-10 ${isActive ? 'bg-theme-text' : 'bg-[#EAE6DD]'}`} />
      
      {/* Pulse Effect for Active Item */}
      {isActive && (
        <motion.div 
          className="absolute left-[7px] sm:left-[19px] top-[6px] w-[10px] h-[10px] rounded-full bg-theme-text z-0 gpu-accelerated"
          animate={{ scale: [1, 2.5], opacity: [0.5, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeOut" }}
        />
      )}

      <h4 className="text-xs sm:text-sm text-theme-muted tracking-widest uppercase mb-1.5 sm:mb-2 flex items-center gap-1.5">
        <span className="text-[10px] opacity-70">{glyph}</span>
        <span>{time}</span>
      </h4>
      <h5 className="font-serif text-2xl sm:text-3xl mb-1 text-theme-text">{title}</h5>
      {subtitle && <p className="text-xs sm:text-sm italic mb-2 text-theme-text">{subtitle}</p>}
      <p className="text-sm sm:text-base text-theme-muted leading-relaxed max-w-xl">{desc}</p>
    </motion.div>
  );
}

function CertCard({ icon, title, issuer, desc }: any) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      whileHover={{ y: -4, scale: 1.01 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className="p-8 sm:p-10 border border-theme-text/10 bg-white/40 backdrop-blur-sm hover:bg-white/60 transition-colors duration-300 interactive rounded-xl flex flex-col gap-4 shadow-sm hover:shadow-md"
    >
      <div className="w-10 h-10 rounded-full bg-theme-text/5 flex items-center justify-center text-theme-text">
        {icon}
      </div>
      <div>
        <h4 className="font-serif text-lg sm:text-xl text-theme-text mb-1">{title}</h4>
        <p className="text-[10px] sm:text-xs uppercase tracking-widest text-theme-muted mb-2.5">{issuer}</p>
        <p className="text-xs sm:text-sm text-theme-text/80 leading-relaxed">{desc}</p>
      </div>
    </motion.div>
  );
}
