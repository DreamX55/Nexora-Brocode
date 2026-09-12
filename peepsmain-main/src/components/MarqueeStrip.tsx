import React from 'react';

export function MarqueeStrip() {
  const items = [
    "Web Development",
    "Creative Engineering",
    "AI / ML",
    "Full Stack",
    "Open to Work",
    "React",
    "Python",
    "Motion Design"
  ];

  return (
    <div className="w-full py-4 border-y border-theme-text/10 overflow-hidden bg-transparent select-none relative z-10">
      <div className="animate-marquee flex items-center whitespace-nowrap">
        {/* Sequence 1 */}
        <div className="flex items-center gap-6 px-4">
          {items.map((item, idx) => (
            <React.Fragment key={`seq1-${idx}`}>
              <span className="text-xs uppercase tracking-[0.3em] text-theme-muted">
                {item}
              </span>
              <span className="text-[10px] text-theme-text/30 select-none">
                ✦
              </span>
            </React.Fragment>
          ))}
        </div>

        {/* Sequence 2 for seamless loop */}
        <div className="flex items-center gap-6 px-4">
          {items.map((item, idx) => (
            <React.Fragment key={`seq2-${idx}`}>
              <span className="text-xs uppercase tracking-[0.3em] text-theme-muted">
                {item}
              </span>
              <span className="text-[10px] text-theme-text/30 select-none">
                ✦
              </span>
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
}
