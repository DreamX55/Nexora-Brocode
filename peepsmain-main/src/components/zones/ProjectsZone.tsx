import React, { useRef } from 'react';
import { motion } from 'motion/react';
import { ArrowUpRight } from 'lucide-react';

const projects = [
  {
    id: "01",
    title: "Student Portfolio",
    purpose: "Personal Branding & Creative Development",
    desc: "A highly interactive personal website designed with motion-first principles, custom cursors, and an immersive user interface.",
    tech: ["React", "Framer Motion", "Tailwind"]
  },
  {
    id: "02",
    title: "Basic Chat App",
    purpose: "Real-time Networking & Comms",
    desc: "A lightweight, real-time messaging application demonstrating client-server communication and socket programming.",
    tech: ["Python", "Sockets"],
    mt: "md:mt-12"
  },
  {
    id: "03",
    title: "To-Do App",
    purpose: "State Management & Productivity",
    desc: "A persistent task management tool utilizing browser storage for stateless data retention across sessions.",
    tech: ["JavaScript", "Local Storage"]
  },
  {
    id: "04",
    title: "Mini AI Chatbot",
    purpose: "Natural Language Processing",
    desc: "An intelligent conversational agent built to process natural language queries and provide context-aware responses.",
    tech: ["Python", "LLM API"],
    mt: "md:mt-12"
  }
];

export function ProjectsZone() {
  const containerRef = useRef<HTMLDivElement>(null);

  return (
    <section id="projects" ref={containerRef} className="py-16 sm:py-20 px-4 sm:px-6 relative flex items-center">
      <div className="max-w-6xl w-full mx-auto">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mb-8 sm:mb-12"
        >
          <div className="flex items-center justify-between mb-3 sm:mb-4">
            <p className="text-xs sm:text-sm tracking-[0.3em] uppercase text-theme-muted">Selected Works</p>
            <span className="text-[10px] uppercase tracking-widest border border-theme-text/20 px-3 py-1 rounded-full text-theme-muted bg-theme-bg/50">
              04 Projects
            </span>
          </div>
          <h2 className="text-4xl sm:text-5xl font-serif italic text-theme-text">Project Showcase.</h2>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
          {projects.map((proj, i) => (
            <motion.div 
              key={proj.id}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: i * 0.1 }}
              className={`border border-theme-text/20 p-6 sm:p-10 relative overflow-hidden group interactive transition-colors duration-500 hover:bg-theme-text hover:text-theme-bg rounded-xl md:rounded-none min-h-[280px] flex flex-col justify-between ${proj.mt || ''}`}
              role="article"
              aria-label={`Project: ${proj.title}`}
            >
              {/* Background Large Faint Watermark Number */}
              <span className="font-serif text-[clamp(80px,12vw,140px)] leading-none text-current opacity-[0.04] absolute right-4 bottom-2 pointer-events-none select-none z-0">
                {proj.id}
              </span>

              {/* Hover Background Accent */}
              <div className="absolute inset-0 bg-theme-text translate-y-full group-hover:translate-y-0 transition-transform duration-700 ease-[0.22,1,0.36,1] z-0 pointer-events-none hidden md:block" />

              <div className="relative z-10 transform transition-transform duration-500 md:group-hover:-translate-y-2">
                <div className="mb-4 sm:mb-6 flex justify-between items-start">
                  <div className="relative inline-block">
                    <h3 className="font-serif text-2xl sm:text-3xl flex items-center gap-3">
                      {proj.title}
                      <ArrowUpRight className="w-5 h-5 sm:w-6 sm:h-6 opacity-80 md:opacity-0 -translate-x-0 translate-y-0 md:-translate-x-4 md:translate-y-4 md:group-hover:opacity-100 md:group-hover:translate-x-0 md:group-hover:translate-y-0 transition-all duration-500 ease-out" />
                    </h3>
                    {/* Animated Underline on Hover */}
                    <div className="h-[1.5px] bg-current w-0 group-hover:w-full transition-all duration-500 ease-out mt-1" />
                  </div>
                  <span className="text-xs uppercase tracking-widest opacity-50 font-mono">{proj.id}</span>
                </div>

                <p className="text-sm sm:text-base text-theme-muted mb-4 sm:mb-6 transition-colors duration-500 md:group-hover:text-theme-bg/80 leading-relaxed">
                  {proj.desc}
                </p>

                <div className="mb-6 sm:mb-8">
                  <p className="text-[9px] uppercase tracking-[0.2em] opacity-60 mb-1">Purpose</p>
                  <p className="text-xs sm:text-sm font-medium">{proj.purpose}</p>
                </div>

                <div className="flex flex-wrap gap-2">
                  {proj.tech.map(t => (
                    <span key={t} className="text-[11px] sm:text-xs border border-current px-2.5 sm:px-3 py-1 rounded-full">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
