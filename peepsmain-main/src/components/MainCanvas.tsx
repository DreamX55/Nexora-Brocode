import React, { lazy, Suspense } from 'react';
import { motion } from 'motion/react';
import { MarqueeStrip } from './MarqueeStrip';

// Lazy loaded zone components for code splitting & optimal loading performance
const AboutZone = lazy(() => import('./zones/AboutZone').then(m => ({ default: m.AboutZone })));
const SkillsZone = lazy(() => import('./zones/SkillsZone').then(m => ({ default: m.SkillsZone })));
const ProjectsZone = lazy(() => import('./zones/ProjectsZone').then(m => ({ default: m.ProjectsZone })));
const EducationZone = lazy(() => import('./zones/EducationZone').then(m => ({ default: m.EducationZone })));
const ContactZone = lazy(() => import('./zones/ContactZone').then(m => ({ default: m.ContactZone })));

function SectionDivider({ label }: { label: string }) {
  return (
    <div className="w-full py-4 flex items-center justify-center relative">
      <div className="absolute inset-0 flex items-center px-6 sm:px-12 pointer-events-none">
        <div className="w-full border-t border-theme-text/10" />
      </div>
      <span className="relative bg-theme-bg px-4 text-[9px] uppercase tracking-[0.3em] text-theme-muted font-sans select-none">
        {label}
      </span>
    </div>
  );
}

export function MainCanvas() {
  return (
    <motion.main 
      role="main"
      className="w-full relative"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1], delay: 0.2 }}
    >
      <Suspense fallback={<div className="w-full min-h-screen bg-theme-bg" />}>
        <div className="flex flex-col">
          <AboutZone />
          <MarqueeStrip />
          <SectionDivider label="· 01 SKILLS ·" />
          <SkillsZone />
          <SectionDivider label="· 02 WORKS ·" />
          <ProjectsZone />
          <SectionDivider label="· 03 MILESTONES ·" />
          <EducationZone />
          <SectionDivider label="· 04 CONNECT ·" />
          <ContactZone />
        </div>
      </Suspense>
    </motion.main>
  );
}
