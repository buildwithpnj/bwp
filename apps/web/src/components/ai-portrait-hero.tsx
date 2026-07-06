'use client';

import React, { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, Github, Twitter, Linkedin, Mail } from 'lucide-react';
import { useTheme } from 'next-themes';
import { AiEcosystemCommandCenter } from './ai-ecosystem-visualization';

interface BGParticle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  alpha: number;
  color: string;
}

export function AIPortraitHero() {
  const { resolvedTheme } = useTheme();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  
  const mouseRef = useRef({ x: -1000, y: -1000, rx: 0, ry: 0, targetRx: 0, targetRy: 0, inside: false });
  const bgParticlesRef = useRef<BGParticle[]>([]);
  
  // Parallax rotation states for heading and buttons
  const [parallax, setParallax] = useState({ x: 0, y: 0 });

  // Typewriter typing animation states for capabilities advertisement
  const [displayText, setDisplayText] = useState('');
  const [phraseIdx, setPhraseIdx] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [cursorVisible, setCursorVisible] = useState(true);
  
  const PHRASES = [
    "AI Agents Building",
    "Voice Agents Development",
    "Workflow Automation",
    "System Designing",
    "UI/UX Product Engineering"
  ];

  // Blinking terminal cursor interval
  useEffect(() => {
    const cursorInterval = setInterval(() => {
      setCursorVisible(v => !v);
    }, 530);
    return () => clearInterval(cursorInterval);
  }, []);

  // Typewriter character addition/deletion speed loop
  useEffect(() => {
    let timer: any;
    const activePhrase = PHRASES[phraseIdx];
    
    if (isDeleting) {
      timer = setTimeout(() => {
        setDisplayText(activePhrase.substring(0, displayText.length - 1));
      }, 35);
    } else {
      timer = setTimeout(() => {
        setDisplayText(activePhrase.substring(0, displayText.length + 1));
      }, 75);
    }

    if (!isDeleting && displayText === activePhrase) {
      // Pause on full phrase display
      timer = setTimeout(() => {
        setIsDeleting(true);
      }, 2200);
    } else if (isDeleting && displayText === '') {
      // Transition to next index
      setIsDeleting(false);
      setPhraseIdx((prev) => (prev + 1) % PHRASES.length);
    }

    return () => clearTimeout(timer);
  }, [displayText, isDeleting, phraseIdx]);

  // Main interactive canvas rendering loop (handles background particles, glow, and grid)
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    let animationFrameId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);
    
    // Initialize background floating particles
    const initBGParticles = () => {
      const pCount = window.innerWidth < 768 ? 30 : 80;
      const bgParticles: BGParticle[] = [];
      const colors = ['#3B82F6', '#06B6D4', '#7C3AED', '#8B5CF6', '#FFFFFF'];
      for (let i = 0; i < pCount; i++) {
        bgParticles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          size: Math.random() * 1.8 + 0.8,
          alpha: Math.random() * 0.4 + 0.15,
          color: colors[Math.floor(Math.random() * colors.length)]
        });
      }
      bgParticlesRef.current = bgParticles;
    };
    initBGParticles();

    // Resize handler
    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      initBGParticles();
    };
    window.addEventListener('resize', handleResize);

    // Cursor tracking
    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      mouseRef.current.x = mx;
      mouseRef.current.y = my;
      mouseRef.current.inside = true;

      // Parallax effect values
      const rx = (mx - width / 2) / (width / 2);
      const ry = (my - height / 2) / (height / 2);
      mouseRef.current.targetRx = rx * 6; // Max 6deg
      mouseRef.current.targetRy = ry * -8; // Max -8deg
    };

    const handleMouseLeave = () => {
      mouseRef.current.inside = false;
      mouseRef.current.targetRx = 0;
      mouseRef.current.targetRy = 0;
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseleave', handleMouseLeave);

    // Animation render loop
    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Smooth springs on parallax mouse values
      mouseRef.current.rx += (mouseRef.current.targetRx - mouseRef.current.rx) * 0.08;
      mouseRef.current.ry += (mouseRef.current.targetRy - mouseRef.current.ry) * 0.08;
      
      setParallax({
        x: mouseRef.current.rx * 2.2,
        y: mouseRef.current.ry * 2.2
      });

      // (A) Living Ambient Neural Gradient Mesh & Volumetric Glow
      const isDark = resolvedTheme === 'dark';
      const time = Date.now() * 0.0006;
      
      const gX = width * 0.5 + Math.sin(time * 0.8) * width * 0.2;
      const gY = height * 0.5 + Math.cos(time * 0.5) * height * 0.2;
      const glowRad = Math.min(width, height) * 0.8;
      
      const ambientGlow = ctx.createRadialGradient(gX, gY, 10, gX, gY, glowRad);
      if (isDark) {
        ambientGlow.addColorStop(0, 'rgba(59, 130, 246, 0.05)'); // Blue
        ambientGlow.addColorStop(0.3, 'rgba(124, 58, 237, 0.025)'); // Purple
        ambientGlow.addColorStop(1, 'rgba(10, 15, 30, 1)'); // Dark Navy
      } else {
        ambientGlow.addColorStop(0, 'rgba(59, 130, 246, 0.03)');
        ambientGlow.addColorStop(0.5, 'rgba(6, 182, 212, 0.015)');
        ambientGlow.addColorStop(1, 'rgba(255, 255, 255, 1)');
      }
      ctx.fillStyle = ambientGlow;
      ctx.fillRect(0, 0, width, height);

      // Draw subtle neural background grid
      ctx.strokeStyle = isDark ? 'rgba(255, 255, 255, 0.012)' : 'rgba(0, 0, 0, 0.018)';
      ctx.lineWidth = 1;
      const gridSize = 45;
      
      // Parallax distortion on background grid
      const gridParallaxX = mouseRef.current.rx * 10;
      const gridParallaxY = mouseRef.current.ry * 10;
      
      ctx.save();
      ctx.translate(gridParallaxX, gridParallaxY);
      
      ctx.beginPath();
      for (let x = 0; x < width; x += gridSize) {
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
      }
      for (let y = 0; y < height; y += gridSize) {
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
      }
      ctx.stroke();
      ctx.restore();

      // (B) Render Floating Background Particles
      bgParticlesRef.current.forEach((bp) => {
        bp.x += bp.vx;
        bp.y += bp.vy;
        
        // Boundary wrap
        if (bp.x < 0) bp.x = width;
        if (bp.x > width) bp.x = 0;
        if (bp.y < 0) bp.y = height;
        if (bp.y > height) bp.y = 0;
        
        // Mouse repelling on background particles
        if (mouseRef.current.inside) {
          const dx = bp.x - mouseRef.current.x;
          const dy = bp.y - mouseRef.current.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 150) {
            const force = (150 - dist) / 150;
            bp.x += (dx / dist) * force * 1.5;
            bp.y += (dy / dist) * force * 1.5;
          }
        }
        
        ctx.fillStyle = bp.color;
        ctx.globalAlpha = bp.alpha;
        ctx.beginPath();
        ctx.arc(bp.x, bp.y, bp.size, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.globalAlpha = 1.0;

      // (C) Cursor Glow Overlay
      const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (mouseRef.current.inside && !isReducedMotion) {
        ctx.save();
        ctx.globalCompositeOperation = 'screen';
        const mouseGlow = ctx.createRadialGradient(mouseRef.current.x, mouseRef.current.y, 0, mouseRef.current.x, mouseRef.current.y, 75);
        mouseGlow.addColorStop(0, 'rgba(6, 182, 212, 0.12)'); // Cyan core
        mouseGlow.addColorStop(0.5, 'rgba(124, 58, 237, 0.03)'); // Purple bloom
        mouseGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = mouseGlow;
        ctx.beginPath();
        ctx.arc(mouseRef.current.x, mouseRef.current.y, 75, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      animationFrameId = requestAnimationFrame(render);
    };
    
    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
      cancelAnimationFrame(animationFrameId);
    };
  }, [resolvedTheme]);

  // Inline 3D parallax styles on container hover
  const transformStyle = {
    transform: `perspective(1000px) rotateX(${parallax.y}deg) rotateY(${parallax.x}deg) translate3d(0, 0, 0)`,
    transition: 'transform 0.25s cubic-bezier(0.16, 1, 0.3, 1)'
  };

  return (
    <section 
      ref={containerRef}
      className="w-screen relative left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] mt-[-32px] md:mt-[-48px] min-h-[100vh] py-16 md:py-0 flex flex-col justify-center overflow-hidden bg-background select-none border-b border-border/20 z-30"
    >
      {/* Background Interactive canvas */}
      <canvas 
        ref={canvasRef}
        className="absolute inset-0 w-full h-full pointer-events-none z-10"
      />

      {/* Readable gradient overlays to blend full-screen backdrop and guarantee high contrast */}
      <div className="absolute inset-0 bg-gradient-to-r from-background via-background/80 to-transparent pointer-events-none z-12 md:w-[70vw] w-full" />
      <div className="absolute inset-0 bg-gradient-to-t from-background/50 via-transparent to-transparent pointer-events-none z-12" />

      {/* Volumetric ambient depth overlay */}
      <div className="absolute inset-0 bg-radial-gradient pointer-events-none z-13" />

      {/* Main Fullscreen Parallax Content Layout */}
      <div 
        style={transformStyle}
        className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center relative z-20"
      >
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center w-full">
          {/* Text block (Left side on large viewport) */}
          <div className="lg:col-span-6 flex flex-col items-start gap-5 text-left max-w-xl">
            
            <div className="font-pixel text-[10px] tracking-[0.25em] text-primary uppercase bg-primary/5 border border-primary/15 px-3 py-1 rounded-full animate-pulse select-none">
              {"// NEURAL SCANNING ACTIVE"}
            </div>

            <h1 className="font-pixel text-4xl sm:text-5xl lg:text-6xl leading-tight tracking-wide text-foreground uppercase select-text">
              Prakash <br />
              <span className="gradient-text">Nandan Jha</span>
            </h1>

            {/* Dynamic Typewriter Advertisement Subtitle */}
            <div className="font-mono text-sm sm:text-base text-foreground/90 flex items-center flex-wrap gap-1.5 select-none min-h-[1.5rem] bg-secondary/30 border border-border/40 px-3 py-1.5 rounded-xl">
              <span className="text-primary font-bold animate-pulse">&gt;</span>
              <span className="text-muted-foreground text-xs">I help with:</span>
              <span className="text-primary font-semibold text-xs sm:text-sm">
                {displayText}
                <span className={`ml-0.5 text-primary font-bold ${cursorVisible ? 'opacity-100' : 'opacity-0'}`}>_</span>
              </span>
            </div>

            <p className="text-sm sm:text-base text-muted-foreground leading-relaxed select-text">
              Building next-generation, production-ready AI products & automated workspaces. Explore active blueprints and R&D pipelines.
            </p>

            <div className="flex flex-col sm:flex-row items-center gap-4 mt-4 w-full sm:w-auto">
              <Link
                href="/projects"
                className="w-full sm:w-auto flex items-center justify-center gap-2 h-11 px-5 rounded-xl text-xs font-semibold bg-primary text-primary-foreground hover:opacity-90 shadow-md shadow-primary/20 transition-all hover:translate-y-[-1px]"
              >
                Launch Blueprints <ArrowRight className="h-3.5 w-3.5" />
              </Link>
              <Link
                href="/journal"
                className="w-full sm:w-auto flex items-center justify-center h-11 px-5 rounded-xl text-xs font-semibold border border-border bg-secondary hover:bg-accent text-muted-foreground hover:text-foreground transition-all hover:translate-y-[-1px]"
              >
                Read Journal
              </Link>
            </div>

            {/* Premium Social Contacts */}
            <div className="flex items-center gap-3.5 mt-4">
              <a href="https://github.com/buildwithpnj" target="_blank" rel="noopener noreferrer" className="p-2.5 rounded-xl border border-border bg-secondary text-muted-foreground hover:text-foreground hover:border-primary/20 transition-all hover:scale-[1.05]">
                <Github className="h-4.5 w-4.5" strokeWidth={1.8} />
              </a>
              <a href="https://twitter.com/buildwithpnj" target="_blank" rel="noopener noreferrer" className="p-2.5 rounded-xl border border-border bg-secondary text-muted-foreground hover:text-foreground hover:border-primary/20 transition-all hover:scale-[1.05]">
                <Twitter className="h-4.5 w-4.5" strokeWidth={1.8} />
              </a>
              <a href="https://linkedin.com/in/pnj" target="_blank" rel="noopener noreferrer" className="p-2.5 rounded-xl border border-border bg-secondary text-muted-foreground hover:text-foreground hover:border-primary/20 transition-all hover:scale-[1.05]">
                <Linkedin className="h-4.5 w-4.5" strokeWidth={1.8} />
              </a>
              <a href="mailto:hello@buildwithpnj.com" className="p-2.5 rounded-xl border border-border bg-secondary text-muted-foreground hover:text-foreground hover:border-primary/20 transition-all hover:scale-[1.05]">
                <Mail className="h-4.5 w-4.5" strokeWidth={1.8} />
              </a>
            </div>

          </div>

          {/* Interactive AI Ecosystem Command Center (Right side on large viewport) */}
          <div className="lg:col-span-6 w-full h-[470px] sm:h-[490px] md:h-[510px] z-20">
            <AiEcosystemCommandCenter />
          </div>
        </div>
      </div>
      
      {/* Scroll indicator overlay */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-20 flex flex-col items-center gap-1.5 opacity-60 hover:opacity-100 transition-opacity">
        <span className="font-pixel text-[9px] tracking-widest text-muted-foreground uppercase">SCROLL TO DISCOVER</span>
        <div className="w-5 h-8 rounded-full border border-border flex justify-center p-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce" />
        </div>
      </div>
    </section>
  );
}
