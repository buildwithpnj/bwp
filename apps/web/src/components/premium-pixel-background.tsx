'use client';

import { useEffect, useRef } from 'react';
import { useTheme } from 'next-themes';

// ─── Types ────────────────────────────────────────────────────────────────────

interface Pixel {
  x: number;
  docY: number;
  vx: number;
  vy: number;
  size: number;
  alpha: number;
  targetAlpha: number;
  hueShift: number;
  satShift: number;
  lightShift: number;
  isWhite: boolean;
  glow: boolean;
  angle: number;
  spin: number;
  snapped: boolean;
  snapT: number;
  sx: number;   // snap start x
  sy: number;   // snap start docY
  tx: number;   // snap target x
  ty: number;   // snap target docY
  flash: number;
  pulse: number;
  alive: boolean; // false = marked for removal
}

interface Slot {
  lx: number;
  ly: number;
  filled: boolean;
}

// ─── Component ────────────────────────────────────────────────────────────────

export function PremiumPixelBackground() {
  const { resolvedTheme } = useTheme();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    const isDark = resolvedTheme === 'dark';

    // Reduced motion
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    let reducedMotion = mq.matches;
    const onMQ = (e: MediaQueryListEvent) => { reducedMotion = e.matches; };
    mq.addEventListener('change', onMQ);

    // Canvas sizing
    let W = window.innerWidth;
    let H = window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, 2); // cap at 2x
    const resize = () => {
      W = window.innerWidth;
      H = window.innerHeight;
      canvas.width = W * dpr;
      canvas.height = H * dpr;
      canvas.style.width = `${W}px`;
      canvas.style.height = `${H}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();
    window.addEventListener('resize', resize);

    // State
    let scrollY = 0;
    let mouseX = -9999;
    let mouseY = -9999;
    let mouseActive = false;
    let primaryH = 221;
    let primaryS = 83;
    let primaryL = 53;
    let frameCount = 0;

    const onScroll = () => { scrollY = window.scrollY; };
    window.addEventListener('scroll', onScroll, { passive: true });

    const onMouse = (e: MouseEvent) => { mouseX = e.clientX; mouseY = e.clientY; mouseActive = true; };
    const onLeave = () => { mouseActive = false; };
    window.addEventListener('mousemove', onMouse, { passive: true });
    document.addEventListener('mouseleave', onLeave);

    // ─── Read --primary (throttled: every 8 frames ≈ 7.5 Hz) ───────────
    const readPrimary = () => {
      const raw = getComputedStyle(document.documentElement).getPropertyValue('--primary');
      if (!raw) return;
      const p = raw.trim().replace(/%/g, '').split(/\s+/);
      if (p.length >= 3) {
        primaryH = +p[0]; primaryS = +p[1]; primaryL = +p[2];
      }
    };
    readPrimary(); // initial read

    // ─── Collection grid (page bottom only) ─────────────────────────────
    let pageBottom = 0;
    let slots: Slot[] = [];
    let gridDone = false;
    let gridTimer = 0;
    let gridFade = 1;
    let scanX = -600;
    let filledCount = 0;

    const buildGrid = () => {
      const dh = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
      pageBottom = dh;
      slots = [];
      filledCount = 0;
      gridDone = false;
      gridTimer = 0;
      gridFade = 1;
      const po = () => Math.random() * 6.28;
      // Bus line
      for (let c = -18; c <= 18; c++) slots.push({ lx: c * 18, ly: -30, filled: false });
      // Branches
      for (const bx of [-216, -144, -72, 0, 72, 144, 216]) {
        for (let r = 1; r <= 4; r++) slots.push({ lx: bx, ly: -30 - r * 14, filled: false });
        slots.push({ lx: bx - 8, ly: -100, filled: false });
        slots.push({ lx: bx + 8, ly: -100, filled: false });
      }
      // Dotted rows
      for (let row = 0; row < 3; row++) {
        const y = -120 - row * 16;
        for (let col = -12; col <= 12; col += 2) {
          if ((col + row) % 3 !== 0) slots.push({ lx: col * 16, ly: y, filled: false });
        }
      }
    };
    buildGrid();
    const gridInterval = setInterval(buildGrid, 6000);

    // ─── Pixel pool (flat array, swap-remove) ───────────────────────────
    const MAX_PIXELS = 200;
    const pixels: Pixel[] = [];

    const removePixel = (i: number) => {
      // Swap with last, pop — O(1)
      const last = pixels.length - 1;
      if (i < last) pixels[i] = pixels[last];
      pixels.pop();
    };

    // Size distribution
    const SIZES = [2,2,2,4,4,4,4,6,6,6,8,8,8,12,12,16,20,24];

    const spawn = () => {
      if (pixels.length >= MAX_PIXELS) return;
      let size = SIZES[(Math.random() * SIZES.length) | 0];
      if (Math.random() < 0.04) size = 28 + ((Math.random() * 2) | 0) * 4; // 28 or 32

      // Spawn position
      let x: number;
      const r = Math.random();
      if (r < 0.35) x = Math.random() * W * 0.18;
      else if (r < 0.70) x = W - Math.random() * W * 0.18;
      else x = Math.random() * W;

      const baseAlpha = size >= 16 ? Math.random() * 0.2 + 0.12 : Math.random() * 0.28 + 0.08;

      pixels.push({
        x,
        docY: scrollY - 30 - Math.random() * 40,
        vx: (Math.random() - 0.5) * 0.3,
        vy: Math.random() * 0.7 + 0.3 + (size >= 16 ? 0.15 : 0),
        size,
        alpha: 0,
        targetAlpha: baseAlpha,
        hueShift: (Math.random() - 0.5) * 20,
        satShift: (Math.random() - 0.5) * 16,
        lightShift: (Math.random() - 0.5) * 24,
        isWhite: Math.random() < 0.06,
        glow: Math.random() < 0.10,
        angle: 0,
        spin: (Math.random() - 0.5) * (size >= 16 ? 0.004 : 0.012),
        snapped: false, snapT: 0,
        sx: 0, sy: 0, tx: 0, ty: 0,
        flash: 0,
        pulse: Math.random() * 0.018 + 0.012,
        alive: true,
      });
    };

    // ─── Pre-computed color cache (updated once per primary read) ────────
    // We'll build a small palette each time primary changes and use index
    let cachedH = -1;
    let cachedS = -1;
    let cachedL = -1;
    // White highlight strings
    const whiteColor = isDark ? 'rgba(255,255,255,0.7)' : 'rgba(255,255,255,0.5)';

    // ─── Render ─────────────────────────────────────────────────────────
    let rafId: number;
    let spawnAccum = 0;

    const render = (time: number) => {
      rafId = requestAnimationFrame(render);
      if (reducedMotion) { ctx.clearRect(0, 0, W, H); return; }

      frameCount++;

      // Throttled primary read (every 8 frames)
      if ((frameCount & 7) === 0) readPrimary();

      ctx.clearRect(0, 0, W, H);

      // Spawn
      spawnAccum++;
      if (spawnAccum >= 12) {
        spawn();
        if (Math.random() < 0.3) spawn();
        spawnAccum = 0;
      }

      // Grid logic
      if (!gridDone) {
        scanX += 2;
        if (scanX > W + 500) scanX = -500 - Math.random() * 300;
        if (filledCount >= slots.length && slots.length > 0) {
          gridDone = true;
          gridTimer = 200;
        }
      } else {
        gridTimer--;
        if (gridTimer <= 80) gridFade = Math.max(0, gridTimer / 80);
        if (gridTimer <= 0) {
          // Reset
          for (let s = 0; s < slots.length; s++) slots[s].filled = false;
          filledCount = 0;
          gridDone = false;
          gridFade = 1;
          // Remove snapped pixels
          for (let i = pixels.length - 1; i >= 0; i--) {
            if (pixels[i].snapped) removePixel(i);
          }
        }
      }

      // Precompute half-width for grid center
      const cx = W * 0.5;

      // ─── Update & Draw ──────────────────────────────────────────────
      for (let i = pixels.length - 1; i >= 0; i--) {
        const p = pixels[i];
        const screenY = p.docY - scrollY;

        // Remove dead or way offscreen free pixels
        if (!p.snapped && p.docY > pageBottom + 200) {
          removePixel(i);
          continue;
        }

        if (!p.snapped) {
          // Fade in
          if (p.alpha < p.targetAlpha) p.alpha += 0.008;

          // Physics
          p.vy += 0.0015;
          p.docY += p.vy;
          p.x += p.vx + Math.sin(time * 0.0008 + p.x * 0.03) * 0.06;
          p.angle += p.spin;

          // Bounds
          if (p.x < -20) p.x = -20;
          else if (p.x > W + 20) p.x = W + 20;

          // Mouse push (squared distance, no sqrt unless close)
          if (mouseActive) {
            const dx = p.x - mouseX;
            const dy = screenY - mouseY;
            const d2 = dx * dx + dy * dy;
            if (d2 < 8100 && d2 > 0) { // 90²
              const dist = Math.sqrt(d2);
              const f = (90 - dist) / 90;
              p.x += (dx / dist) * f;
              p.docY += (dy / dist) * f * 0.4;
            }
          }

          // Grid snap check
          if (!gridDone && p.docY >= pageBottom - 180 && p.docY <= pageBottom + 20) {
            let bestIdx = -1;
            let bestD = Infinity;
            for (let s = 0; s < slots.length; s++) {
              if (slots[s].filled) continue;
              const dx = (cx + slots[s].lx) - p.x;
              const dy = (pageBottom + slots[s].ly) - p.docY;
              const d = dx * dx + dy * dy;
              if (d < bestD) { bestD = d; bestIdx = s; }
            }
            if (bestIdx >= 0) {
              const sl = slots[bestIdx];
              sl.filled = true;
              filledCount++;
              p.snapped = true;
              p.sx = p.x; p.sy = p.docY;
              p.tx = cx + sl.lx; p.ty = pageBottom + sl.ly;
              p.snapT = 0.01;
              if (Math.random() < 0.35) p.flash = 20;
            }
          }

          // Remove if past bottom with no slot
          if (p.docY > pageBottom + 200) { removePixel(i); continue; }
        } else {
          // Snap lerp
          if (p.snapT < 1) {
            p.snapT += 0.05;
            if (p.snapT >= 1) {
              p.snapT = 1; p.x = p.tx; p.docY = p.ty;
            } else {
              const t = 1 - (1 - p.snapT) * (1 - p.snapT) * (1 - p.snapT); // ease-out cubic
              p.x = p.sx + (p.tx - p.sx) * t;
              p.docY = p.sy + (p.ty - p.sy) * t;
            }
          }
        }

        // ─── Draw ───────────────────────────────────────────────────
        const dy = p.docY - scrollY;
        if (dy > H + 40 || dy < -40) continue;

        let a = p.alpha;
        let isFlash = false;

        if (p.snapped) {
          a *= gridFade;
          if (p.snapT >= 1 && !gridDone) {
            a = Math.max(0.06, Math.min(0.7, p.alpha + Math.sin(time * p.pulse + p.x * 0.1) * 0.1));
          }
          const sd = scanX - p.x;
          if (sd > -70 && sd < 70) {
            a = Math.min(1, a + (1 - Math.abs(sd) / 70) * 0.4);
            isFlash = true;
          }
        }

        if (p.flash > 0) {
          p.flash--;
          a = Math.min(1, a + (p.flash / 20) * 0.5);
          isFlash = true;
        }

        // Compute color from live primary
        let color: string;
        if (p.isWhite) {
          color = whiteColor;
        } else {
          const h = ((primaryH + p.hueShift) % 360 + 360) % 360;
          const s = Math.max(0, Math.min(100, primaryS + p.satShift));
          const l = Math.max(10, Math.min(90, primaryL + p.lightShift));
          color = `hsl(${h},${s}%,${l}%)`;
        }

        ctx.globalAlpha = a;

        if (p.glow || isFlash) {
          ctx.shadowColor = color;
          ctx.shadowBlur = p.size * 0.5;
        } else {
          ctx.shadowBlur = 0;
        }

        ctx.fillStyle = isFlash ? '#FFF' : color;

        if (!p.snapped && p.angle !== 0) {
          ctx.save();
          ctx.translate(p.x, dy);
          ctx.rotate(p.angle);
          const half = p.size * 0.5;
          ctx.fillRect(-half, -half, p.size, p.size);
          ctx.restore();
        } else {
          const half = p.size * 0.5;
          ctx.fillRect(p.x - half, dy - half, p.size, p.size);
        }
      }

      // Reset composite state
      ctx.globalAlpha = 1;
      ctx.shadowBlur = 0;
    };

    rafId = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(rafId);
      mq.removeEventListener('change', onMQ);
      window.removeEventListener('resize', resize);
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('mousemove', onMouse);
      document.removeEventListener('mouseleave', onLeave);
      clearInterval(gridInterval);
    };
  }, [resolvedTheme]);

  return (
    <div className="fixed inset-0 w-full h-full pointer-events-none z-[11] overflow-hidden">
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full pointer-events-none"
      />
    </div>
  );
}
