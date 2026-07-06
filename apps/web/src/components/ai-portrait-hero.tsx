'use client';

import React, { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { ArrowRight, Github, Twitter, Linkedin, Mail, Command } from 'lucide-react';
import { useTheme } from 'next-themes';

interface Particle {
  x: number;
  y: number;
  ox: number;
  oy: number;
  color: { r: number; g: number; b: number };
  targetColor: { r: number; g: number; b: number };
  colorTransition: number;
  vx: number;
  vy: number;
  size: number;
  originalSize: number;
  alpha: number;
  originalAlpha: number;
  angle: number;
  spin: number;
  active: boolean;
  detached?: boolean;
  detachTimer?: number;
}

interface BGParticle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  alpha: number;
  color: string;
}

interface Ember {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  originalSize: number;
  alpha: number;
  color: { r: number; g: number; b: number };
  life: number;
  maxLife: number;
  swaySpeed: number;
  swayOffset: number;
}

export function AIPortraitHero() {
  const { resolvedTheme } = useTheme();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  
  const [portraits, setPortraits] = useState<string[]>([]);
  const [activePortrait, setActivePortrait] = useState<string>('');
  const [loading, setLoading] = useState(true);
  
  const mouseRef = useRef({ x: -1000, y: -1000, rx: 0, ry: 0, targetRx: 0, targetRy: 0, inside: false });
  const particlesRef = useRef<Particle[]>([]);
  const bgParticlesRef = useRef<BGParticle[]>([]);
  const embersRef = useRef<Ember[]>([]);
  const layoutRef = useRef({ xOffset: 0, yOffset: 0, targetWidth: 0, targetHeight: 0 });
  const scanRef = useRef({ active: false, y: 0, progress: 0, timer: 0 });
  const morphProgressRef = useRef(1.0); // 1.0 = fully morphed
  
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

  // 1. Fetch portraits from dynamic API
  useEffect(() => {
    async function loadPortraits() {
      try {
        const res = await fetch('/api/portraits');
        const data = await res.json();
        if (data.portraits && data.portraits.length > 0) {
          setPortraits(data.portraits);
          // Random portrait on load
          const randomIdx = Math.floor(Math.random() * data.portraits.length);
          setActivePortrait(data.portraits[randomIdx]);
        } else {
          // Fallback to placeholder if folder is empty or not loaded yet
          setPortraits(['/assets/images/Man_looking_directly_camera_2K_202607061917.jpeg']);
          setActivePortrait('/assets/images/Man_looking_directly_camera_2K_202607061917.jpeg');
        }
      } catch (err) {
        console.error('Failed to load portraits:', err);
        setPortraits(['/assets/images/Man_looking_directly_camera_2K_202607061917.jpeg']);
        setActivePortrait('/assets/images/Man_looking_directly_camera_2K_202607061917.jpeg');
      } finally {
        setLoading(false);
      }
    }
    loadPortraits();
  }, []);

  // 2. Crossfade/Morph interval
  useEffect(() => {
    if (portraits.length <= 1) return;
    
    const interval = setInterval(() => {
      // Choose a different random portrait
      setActivePortrait((current) => {
        const remaining = portraits.filter(p => p !== current);
        if (remaining.length === 0) return current;
        const randomIdx = Math.floor(Math.random() * remaining.length);
        return remaining[randomIdx];
      });
    }, 12000); // Morph every 12 seconds
    
    return () => clearInterval(interval);
  }, [portraits]);

  // 3. Main interactive canvas rendering loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    let animationFrameId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);
    
    // Set offscreen canvas for downsampling
    const offscreenCanvas = document.createElement('canvas');
    const offscreenCtx = offscreenCanvas.getContext('2d');
    
    let activeImage: HTMLImageElement | null = null;
    let isTransitioning = false;
    
    // Initialize background floating particles
    const initBGParticles = () => {
      const pCount = window.innerWidth < 768 ? 40 : 120;
      const bgParticles: BGParticle[] = [];
      const colors = ['#3B82F6', '#06B6D4', '#7C3AED', '#8B5CF6', '#FFFFFF'];
      for (let i = 0; i < pCount; i++) {
        bgParticles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * 0.4,
          vy: (Math.random() - 0.5) * 0.4,
          size: Math.random() * 2 + 1,
          alpha: Math.random() * 0.5 + 0.1,
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
      if (activeImage) {
        processImage(activeImage);
      }
    };
    window.addEventListener('resize', handleResize);

    // Process active image and initialize/morph face particles to cover the entire viewport (cover)
    const processImage = (img: HTMLImageElement) => {
      if (!offscreenCtx) return;
      
      // Use a slightly stretched fixed aspect ratio (0.9) to make the headshot wider on screen
      const targetAspect = 0.9;
      const canvasAspect = width / height;
      
      let targetWidth = 0;
      let targetHeight = 0;
      let xOffset = 0;
      let yOffset = 0;
      
      if (targetAspect > canvasAspect) {
        // Target is wider than viewport aspect ratio -> fit by width (contain)
        targetWidth = width;
        targetHeight = width / targetAspect;
        xOffset = 0;
        yOffset = (height - targetHeight) / 2;
      } else {
        // Target is taller than or equal to viewport aspect ratio -> fit by height (contain)
        targetHeight = height;
        targetWidth = height * targetAspect;
        xOffset = (width - targetWidth) / 2;
        yOffset = 0;
      }
      
      // Store current sizing details in layoutRef for ember spawning
      layoutRef.current = { xOffset, yOffset, targetWidth, targetHeight };
      
      offscreenCanvas.width = 130; // Downsample resolution width (fixed matching targetAspect)
      offscreenCanvas.height = Math.round(130 / targetAspect);
      
      offscreenCtx.clearRect(0, 0, offscreenCanvas.width, offscreenCanvas.height);
      offscreenCtx.drawImage(img, 0, 0, offscreenCanvas.width, offscreenCanvas.height);
      
      const imgData = offscreenCtx.getImageData(0, 0, offscreenCanvas.width, offscreenCanvas.height);
      const data = imgData.data;
      
      const newParticles: Particle[] = [];
      const cellWidth = targetWidth / offscreenCanvas.width;
      const cellHeight = targetHeight / offscreenCanvas.height;
      
      const centerX = offscreenCanvas.width / 2;
      const centerY = offscreenCanvas.height / 2;
      const maxDist = Math.sqrt(centerX * centerX + centerY * centerY);

      // Scan through downsampled pixel grid
      for (let y = 0; y < offscreenCanvas.height; y++) {
        for (let x = 0; x < offscreenCanvas.width; x++) {
          const idx = (y * offscreenCanvas.width + x) * 4;
          const r = data[idx];
          const g = data[idx+1];
          const b = data[idx+2];
          const a = data[idx+3];
          
          const brightness = (r + g + b) / 3;
          
          // Since background is already transparent in the new PNGs, map non-transparent pixels directly
          if (a > 30 && brightness > 10) {
            let pSize = Math.random() * 2 + 3.2;
            let pAlpha = Math.random() * 0.4 + 0.6;
            
            // Soften the sharp bottom boundary crop of the suit/chest using a smooth opacity fade-out (no skipping particles)
            const fadeZoneHeight = Math.round(offscreenCanvas.height * 0.12);
            const startFadeY = offscreenCanvas.height - fadeZoneHeight;
            
            if (y > startFadeY) {
              const fraction = Math.min(1.0, Math.max(0.0, (y - startFadeY) / fadeZoneHeight));
              const fade = 1.0 - fraction;
              pAlpha *= fade; // Linear fade to zero opacity at the very bottom edge
              pSize *= (0.75 + fade * 0.25); // Gentle size shrink
            }
            
            const px = x * cellWidth + xOffset;
            const py = y * cellHeight + yOffset;
            
            newParticles.push({
              x: px,
              y: py,
              ox: px,
              oy: py,
              color: { r, g, b },
              targetColor: { r, g, b },
              colorTransition: 1.0,
              vx: 0,
              vy: 0,
              size: pSize,
              originalSize: pSize,
              alpha: pAlpha,
              originalAlpha: pAlpha,
              angle: Math.random() * Math.PI * 2,
              spin: (Math.random() - 0.5) * 0.05,
              active: true,
              detached: false,
              detachTimer: 0
            });
          }
        }
      }

      // If particles already exist, morph colors & apply turbulence instead of clearing
      if (particlesRef.current.length > 0) {
        const oldP = particlesRef.current;
        const count = Math.min(oldP.length, newParticles.length);
        
        // Morphed existing particles
        for (let i = 0; i < count; i++) {
          oldP[i].ox = newParticles[i].ox;
          oldP[i].oy = newParticles[i].oy;
          oldP[i].targetColor = newParticles[i].color;
          oldP[i].originalAlpha = newParticles[i].originalAlpha;
          oldP[i].originalSize = newParticles[i].originalSize;
          oldP[i].colorTransition = 0;
          
          // Apply slight dispersion force on morph transition
          oldP[i].vx += (Math.random() - 0.5) * 5;
          oldP[i].vy += (Math.random() - 0.5) * 5;
        }
        
        // If we have more new particles, append them
        if (newParticles.length > oldP.length) {
          particlesRef.current = [...oldP, ...newParticles.slice(oldP.length)];
        } else if (newParticles.length < oldP.length) {
          // Truncate list smoothly
          particlesRef.current = oldP.slice(0, newParticles.length);
        }
        
        morphProgressRef.current = 0;
      } else {
        particlesRef.current = newParticles;
      }
    };

    // Load active image
    if (activePortrait) {
      activeImage = new Image();
      activeImage.src = activePortrait;
      activeImage.onload = () => {
        processImage(activeImage!);
      };
    }

    // 4. Cursor tracking & rotation triggers
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

    // Dynamic AI scan trigger
    let scanInterval = setInterval(() => {
      if (!scanRef.current.active) {
        scanRef.current.active = true;
        scanRef.current.progress = 0;
        scanRef.current.y = 0;
      }
    }, 22000); // Scan every 22 seconds

    // 5. Animation render loop
    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Smooth springs on parallax mouse values
      mouseRef.current.rx += (mouseRef.current.targetRx - mouseRef.current.rx) * 0.08;
      mouseRef.current.ry += (mouseRef.current.targetRy - mouseRef.current.ry) * 0.08;
      
      setParallax({
        x: mouseRef.current.rx * 2.5,
        y: mouseRef.current.ry * 2.5
      });

      // (A) Living Ambient Neural Gradient Mesh & Volumetric Glow
      const isDark = resolvedTheme === 'dark';
      const time = Date.now() * 0.0006;
      
      const gX = width * 0.5 + Math.sin(time * 0.8) * width * 0.2;
      const gY = height * 0.5 + Math.cos(time * 0.5) * height * 0.2;
      const glowRad = Math.min(width, height) * 0.8;
      
      const ambientGlow = ctx.createRadialGradient(gX, gY, 10, gX, gY, glowRad);
      if (isDark) {
        ambientGlow.addColorStop(0, 'rgba(59, 130, 246, 0.06)'); // Blue
        ambientGlow.addColorStop(0.3, 'rgba(124, 58, 237, 0.03)'); // Purple
        ambientGlow.addColorStop(1, 'rgba(10, 15, 30, 1)'); // Dark Navy
      } else {
        ambientGlow.addColorStop(0, 'rgba(59, 130, 246, 0.04)');
        ambientGlow.addColorStop(0.5, 'rgba(6, 182, 212, 0.02)');
        ambientGlow.addColorStop(1, 'rgba(255, 255, 255, 1)');
      }
      ctx.fillStyle = ambientGlow;
      ctx.fillRect(0, 0, width, height);

      // Draw subtle neural background grid
      ctx.strokeStyle = isDark ? 'rgba(255, 255, 255, 0.02)' : 'rgba(0, 0, 0, 0.025)';
      ctx.lineWidth = 1;
      const gridSize = 40;
      
      // Parallax distortion on background grid
      const gridParallaxX = mouseRef.current.rx * 12;
      const gridParallaxY = mouseRef.current.ry * 12;
      
      ctx.save();
      ctx.translate(gridParallaxX, gridParallaxY);
      
      // Render pixelated grid during identity scans
      const isPixelatedMode = scanRef.current.active && scanRef.current.progress > 0.15 && scanRef.current.progress < 0.65;
      
      if (isPixelatedMode) {
        ctx.fillStyle = isDark ? 'rgba(59, 130, 246, 0.015)' : 'rgba(0, 0, 0, 0.015)';
        for (let gx = 0; gx < width; gx += 80) {
          for (let gy = 0; gy < height; gy += 80) {
            if (Math.random() > 0.4) {
              ctx.fillRect(gx, gy, 70, 70);
            }
          }
        }
      } else {
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
      }
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
            bp.x += (dx / dist) * force * 2;
            bp.y += (dy / dist) * force * 2;
          }
        }
        
        ctx.fillStyle = bp.color;
        ctx.globalAlpha = bp.alpha;
        ctx.beginPath();
        ctx.arc(bp.x, bp.y, bp.size, 0, Math.PI * 2);
        ctx.fill();
      });
      ctx.globalAlpha = 1.0;

      // (C) Update scan state
      if (scanRef.current.active) {
        scanRef.current.progress += 0.012; // Complete scan over ~2 seconds
        scanRef.current.y = scanRef.current.progress * height;
        
        if (scanRef.current.progress >= 1.0) {
          scanRef.current.active = false;
        }
      }

      // (D) Update morph color transition
      if (morphProgressRef.current < 1.0) {
        morphProgressRef.current += 0.03;
      }

      // (E) Render Face Portrait Downsampled Particles
      const particles = particlesRef.current;
      const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      
      const mouseX = mouseRef.current.x;
      const mouseY = mouseRef.current.y;
      
      // Calculate idle breathing values
      const breathScale = 1.0 + Math.sin(time * 1.5) * 0.012;
      const breathRotate = Math.sin(time * 0.5) * 0.005;

      ctx.save();
      // Set blending mode: screen (glow) in dark mode, normal (source-over) in light mode to keep pixels visible
      ctx.globalCompositeOperation = resolvedTheme === 'light' ? 'source-over' : 'screen';

      // Randomly detach a few particles to create the floating/glowing self-assembly flow
      // Randomly detach a few particles to create the floating/glowing self-assembly flow
      if (!isReducedMotion && Math.random() < 0.28 && particles.length > 0) {
        const detachCount = Math.floor(Math.random() * 2) + 1;
        for (let k = 0; k < detachCount; k++) {
          const randIdx = Math.floor(Math.random() * particles.length);
          const p = particles[randIdx];
          if (p && !p.detached) {
            // Anchor check: particles in the bottom region have lower/zero chance of detaching
            let canDetach = true;
            if (layoutRef.current.targetHeight > 0) {
              const bottomY = layoutRef.current.yOffset + layoutRef.current.targetHeight;
              const distToBottom = bottomY - p.oy;
              const stability = Math.max(0.0, Math.min(1.0, distToBottom / (layoutRef.current.targetHeight * 0.40)));
              if (stability < 0.15 || Math.random() > stability) {
                canDetach = false;
              }
            }
            if (canDetach) {
              p.detached = true;
              p.detachTimer = 100 + Math.random() * 110; // ~2-3.5 seconds
            }
          }
        }
      }

      particles.forEach((p) => {
        // Linear morph color interpolation
        if (p.colorTransition < 1.0) {
          p.colorTransition += 0.03;
          p.color.r += (p.targetColor.r - p.color.r) * p.colorTransition;
          p.color.g += (p.targetColor.g - p.color.g) * p.colorTransition;
          p.color.b += (p.targetColor.b - p.color.b) * p.colorTransition;
        }
        
        // Calculate stability anchor factor at the bottom of the portrait layout (0.0 = fully static base, 1.0 = fully dynamic upper zone)
        let stabilityFactor = 1.0;
        if (layoutRef.current.targetHeight > 0) {
          const bottomY = layoutRef.current.yOffset + layoutRef.current.targetHeight;
          const distToBottom = bottomY - p.oy;
          // Anchor the bottom 40% height of the portrait
          stabilityFactor = Math.max(0.0, Math.min(1.0, distToBottom / (layoutRef.current.targetHeight * 0.40)));
          stabilityFactor = Math.pow(stabilityFactor, 2); // Quadratic ease for smoother transition
        }
        
        // 1. Core target alignment with idle breathing & parallax
        let targetX = p.ox;
        let targetY = p.oy;
        
        if (!isReducedMotion) {
          // Dynamic scaling / rotation offset (Breathe) around screen center
          const dx = p.ox - width * 0.5;
          const dy = p.oy - height * 0.5;
          const rx = dx * Math.cos(breathRotate) - dy * Math.sin(breathRotate);
          const ry = dx * Math.sin(breathRotate) + dy * Math.cos(breathRotate);
          
          const breatheTargetX = rx * breathScale + width * 0.5;
          const breatheTargetY = ry * breathScale + height * 0.5;
          
          const parallaxOffsetX = mouseRef.current.rx * 8;
          const parallaxOffsetY = mouseRef.current.ry * 8;
          
          // Apply stabilityFactor to breathing and parallax offsets so bottom is 100% stationary
          targetX = p.ox + (breatheTargetX - p.ox + parallaxOffsetX) * stabilityFactor;
          targetY = p.oy + (breatheTargetY - p.oy + parallaxOffsetY) * stabilityFactor;
        }

        // 2. Cursor Intelligence Interaction (Pixel detach/scatter)
        if (mouseRef.current.inside && !isReducedMotion) {
          const dx = p.x - mouseX;
          const dy = p.y - mouseY;
          const dist = Math.sqrt(dx * dx + dy * dy);
          
          if (dist < 55) {
            // Stronger push closer to cursor (Repel) - tighter, smaller radius
            const repelForce = (55 - dist) / 55;
            const pushX = (dx / dist) * repelForce * 8 * stabilityFactor;
            const pushY = (dy / dist) * repelForce * 8 * stabilityFactor;
            
            p.vx += pushX;
            p.vy += pushY;
            p.angle += p.spin * repelForce * 2 * stabilityFactor;
            
            // Pulse particle size on hover (scaled by stability)
            p.size = p.originalSize * (1.0 + repelForce * 0.4 * stabilityFactor);
          }
        }

        // 3. Digital Scan wave impact
        if (scanRef.current.active && !isReducedMotion) {
          const scanDist = Math.abs(p.y - scanRef.current.y);
          if (scanDist < 60) {
            const waveForce = (60 - scanDist) / 60;
            // Explode outward laterally (scaled by stability)
            p.vx += (Math.random() - 0.5) * waveForce * 16 * stabilityFactor;
            p.vy += (Math.random() - 0.5) * waveForce * 4 * stabilityFactor;
            p.alpha = Math.max(0.2, p.alpha - waveForce * 0.4 * stabilityFactor);
          }
        }

        // 4. Applying physics / friction / spring forces to target
        if (p.detached) {
          p.detachTimer!--;
          if (p.detachTimer! <= 0) {
            p.detached = false;
          }
          
          // Drift physics (glowing float phase)
          p.vx += (Math.random() - 0.5) * 0.28;
          p.vy += (Math.random() - 0.5) * 0.16 - 0.08; // float upwards bias
          p.vx *= 0.94;
          p.vy *= 0.94;
          
          p.x += p.vx;
          p.y += p.vy;
          
          // Detached particles become larger, bright glowing sparks
          p.size += (p.originalSize * 1.4 - p.size) * 0.06;
          p.alpha += (1.0 - p.alpha) * 0.1;
        } else {
          if (isReducedMotion) {
            p.x = targetX;
            p.y = targetY;
            p.vx = 0;
            p.vy = 0;
          } else {
            const springF = 0.08;
            const friction = 0.82;
            
            const forceX = (targetX - p.x) * springF;
            const forceY = (targetY - p.y) * springF;
            
            p.vx = (p.vx + forceX) * friction;
            p.vy = (p.vy + forceY) * friction;
            
            p.x += p.vx;
            p.y += p.vy;
            
            // Reconstruct values slowly back to original grid sizes and opacity fade profiles
            p.size += (p.originalSize - p.size) * 0.08;
            p.alpha += (p.originalAlpha - p.alpha) * 0.08;
          }
        }

        // 5. Drawing particle pixel
        const cr = Math.round(p.color.r);
        const cg = Math.round(p.color.g);
        const cb = Math.round(p.color.b);
        
        // A. Draw soft backing glow (bloom halo) for photo pixels only (only in dark mode to prevent muddiness in light mode)
        if (resolvedTheme !== 'light') {
          ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${p.alpha * 0.35})`;
          ctx.fillRect(p.x - p.size, p.y - p.size, p.size * 2, p.size * 2);
        }
        
        // B. Draw crisp main square pixel on top
        ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${p.alpha})`;
        ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size);
      });
      ctx.restore();

      // (EE) Spawn and Render Rising Energy Embers
      if (!isReducedMotion) {
        const layout = layoutRef.current;
        if (layout.targetWidth > 0) {
          // Spawn 1-2 embers per frame
          const spawnCount = Math.random() < 0.4 ? 2 : 1;
          for (let i = 0; i < spawnCount; i++) {
            // Spawn at the bottom fade zone of the portrait layout bounds
            const spawnX = layout.xOffset + Math.random() * layout.targetWidth;
            const spawnY = layout.yOffset + layout.targetHeight - Math.random() * (layout.targetHeight * 0.12);
            
            const speed = Math.random() * 1.8 + 1.2;
            const originalSize = Math.random() * 2.5 + 2.0; // Embers are 2px to 4.5px
            
            // Randomly select vibrant theme colors (cyan, blue, purple)
            const colors = [
              { r: 6, g: 182, b: 212 },  // Cyan
              { r: 59, g: 130, b: 246 }, // Blue
              { r: 124, g: 58, b: 237 }  // Purple
            ];
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            embersRef.current.push({
              x: spawnX,
              y: spawnY,
              vx: (Math.random() - 0.5) * 0.5,
              vy: -speed, // Rising speed
              size: originalSize,
              originalSize,
              alpha: Math.random() * 0.4 + 0.6,
              color,
              life: 90 + Math.random() * 60, // frames
              maxLife: 150,
              swaySpeed: Math.random() * 0.04 + 0.02,
              swayOffset: Math.random() * Math.PI * 2
            });
          }
        }

        // Draw and update embers
        ctx.save();
        ctx.globalCompositeOperation = resolvedTheme === 'light' ? 'source-over' : 'screen';
        
        embersRef.current = embersRef.current.filter((ember) => {
          ember.life--;
          if (ember.life <= 0) return false;
          
          ember.y += ember.vy;
          ember.x += Math.sin(time * 2 + ember.swayOffset) * 0.45 + ember.vx;
          
          const lifeRatio = ember.life / ember.maxLife;
          ember.alpha = Math.min(1.0, lifeRatio * 1.6);
          ember.size = ember.originalSize * (0.35 + lifeRatio * 0.65);
          
          const cr = ember.color.r;
          const cg = ember.color.g;
          const cb = ember.color.b;
          
          // Draw soft glow under ember (only in dark mode)
          if (resolvedTheme !== 'light') {
            ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${ember.alpha * 0.35})`;
            ctx.fillRect(ember.x - ember.size, ember.y - ember.size, ember.size * 2, ember.size * 2);
          }
          
          ctx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${ember.alpha})`;
          ctx.fillRect(ember.x - ember.size / 2, ember.y - ember.size / 2, ember.size, ember.size);
          
          return true;
        });
        
        ctx.restore();
      }

      // (F) Draw Horizontal Identity Scan line overlay
      if (scanRef.current.active && !isReducedMotion) {
        ctx.save();
        ctx.shadowBlur = 15;
        ctx.shadowColor = '#06B6D4';
        
        const scanGrad = ctx.createLinearGradient(0, scanRef.current.y - 12, 0, scanRef.current.y + 12);
        scanGrad.addColorStop(0, 'rgba(6, 182, 212, 0)');
        scanGrad.addColorStop(0.5, 'rgba(6, 182, 212, 0.7)');
        scanGrad.addColorStop(1, 'rgba(6, 182, 212, 0)');
        
        ctx.fillStyle = scanGrad;
        ctx.fillRect(0, scanRef.current.y - 12, width, 24);
        ctx.restore();
      }

      // (G) Cursor Energy Trail & Light source glow
      if (mouseRef.current.inside && !isReducedMotion) {
        ctx.save();
        ctx.globalCompositeOperation = 'screen';
        const mouseGlow = ctx.createRadialGradient(mouseX, mouseY, 0, mouseX, mouseY, 75);
        mouseGlow.addColorStop(0, 'rgba(6, 182, 212, 0.15)'); // Cyan core
        mouseGlow.addColorStop(0.5, 'rgba(124, 58, 237, 0.04)'); // Purple bloom
        mouseGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = mouseGlow;
        ctx.beginPath();
        ctx.arc(mouseX, mouseY, 75, 0, Math.PI * 2);
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
      clearInterval(scanInterval);
      cancelAnimationFrame(animationFrameId);
    };
  }, [activePortrait, resolvedTheme]);

  // 6. Inline 3D parallax styles on container hover
  const transformStyle = {
    transform: `perspective(1000px) rotateX(${parallax.y}deg) rotateY(${parallax.x}deg) translate3d(0, 0, 0)`,
    transition: 'transform 0.25s cubic-bezier(0.16, 1, 0.3, 1)'
  };

  return (
    <section 
      ref={containerRef}
      className="w-screen relative left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] mt-[-32px] md:mt-[-48px] h-[100vh] flex flex-col justify-center overflow-hidden bg-background select-none border-b border-border/20 z-30"
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
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center w-full">
          {/* Text block (Left side on large viewport) */}
          <div className="md:col-span-6 flex flex-col items-start gap-5 text-left max-w-xl">
            
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
