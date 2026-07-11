'use client';

import React, { useEffect, useRef, useState, useCallback } from 'react';
import { useTheme } from 'next-themes';

// ─── Interfaces ───────────────────────────────────────────────────────────────

interface SubSystemNode {
  id: string;
  label: string;
  sectionId: string;
  align: 'left' | 'right';
  yOffset: number;
  status: string;
  pulseTimer: number;
}

interface Packet {
  pathIndex: number;
  segmentIndex: number;
  progress: number; // 0 to 1 along segment
  speed: number;
  size: number;
  alpha: number;
  isMaster: boolean;
  label: string;
  category: 'request' | 'inference' | 'memory' | 'broadcast' | 'success' | 'retry' | 'error';
  colorOverride?: string;
  lifeTime?: number;
}

interface CircuitSegment {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

interface CircuitPath {
  id: string;
  segments: CircuitSegment[];
  length: number;
}

interface ExclusionZone {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  padding: number;
  id: string;
}

function getSegmentOpacityMultiplier(x1: number, y1: number, x2: number, y2: number, zones: ExclusionZone[]): number {
  let minMultiplier = 1.0;
  const segMinX = Math.min(x1, x2);
  const segMaxX = Math.max(x1, x2);
  const segMinY = Math.min(y1, y2);
  const segMaxY = Math.max(y1, y2);

  for (let i = 0; i < zones.length; i++) {
    const zone = zones[i];
    const zx1 = zone.x1 - zone.padding;
    const zx2 = zone.x2 + zone.padding;
    const zy1 = zone.y1 - zone.padding;
    const zy2 = zone.y2 + zone.padding;

    // Check box overlap
    const overlapX = segMinX <= zx2 && segMaxX >= zx1;
    const overlapY = segMinY <= zy2 && segMaxY >= zy1;

    if (overlapX && overlapY) {
      minMultiplier = Math.min(minMultiplier, 0.08);
    }
  }
  return minMultiplier;
}

function getPacketOpacityMultiplier(x: number, y: number, zones: ExclusionZone[]): number {
  let minMultiplier = 1.0;
  for (let i = 0; i < zones.length; i++) {
    const zone = zones[i];
    const zx1 = zone.x1 - zone.padding;
    const zx2 = zone.x2 + zone.padding;
    const zy1 = zone.y1 - zone.padding;
    const zy2 = zone.y2 + zone.padding;

    if (x >= zx1 && x <= zx2 && y >= zy1 && y <= zy2) {
      minMultiplier = Math.min(minMultiplier, 0.1);
    }
  }
  return minMultiplier;
}

// ─── Telemetry Label Configurations ──────────────────────────────────────────

const PACKET_LABES = {
  request: ['REQ', 'ACK', 'RSP', 'API', 'POST', 'GET', 'PUT', 'JSON', 'JWT', 'AUTH'],
  inference: ['LLM', 'RAG', 'MCP', 'TOK', 'EMB', 'MODEL', 'PLAN', 'EXEC'],
  memory: ['MEM', 'CTX', 'VECTOR', 'SEARCH', 'SQL', 'CACHE'],
  broadcast: ['SYNC', 'PING', 'PONG', 'WEBHOOK', 'QUEUE'],
  success: ['200 OK', 'DONE', 'COMPLETE'],
  retry: ['RETRY', 'TIMEOUT'],
  error: ['LOST', '404 ERR', '500 ERR']
};

const FOOTER_STATUSES = [
  'SYSTEM ONLINE',
  'ALL SERVICES HEALTHY',
  'LATENCY 18ms',
  'AGENTS READY',
  'MEMORY SYNC COMPLETE',
  'BUILDWITHPNJ ACTIVE'
];

const SUBSYSTEM_NODES: SubSystemNode[] = [
  { id: 'hero-core', label: 'WARBORN PROCESSOR', sectionId: 'section-hero', align: 'left', yOffset: 128, status: 'SYS ACTIVE', pulseTimer: 0 },
  { id: 'voice-ai', label: 'VOICE AI ENGINE', sectionId: 'section-mission', align: 'left', yOffset: 32, status: 'VOICE READY', pulseTimer: 0 },
  { id: 'solutions-mem', label: 'MEMORY SYNC', sectionId: 'section-solutions', align: 'right', yOffset: 64, status: 'PERSISTENT', pulseTimer: 0 },
  { id: 'projects-router', label: 'SHIPS TELEMETRY', sectionId: 'section-projects', align: 'left', yOffset: 96, status: 'MONITORED', pulseTimer: 0 },
  { id: 'labs-compute', label: 'R&D COMPUTE', sectionId: 'section-labs', align: 'right', yOffset: 64, status: 'COMPILING', pulseTimer: 0 },
  { id: 'journal-log', label: 'ENGINE JOURNAL', sectionId: 'section-journal', align: 'left', yOffset: 64, status: 'ARCHIVED', pulseTimer: 0 },
  { id: 'mission-status', label: 'RUN TIME WATCH', sectionId: 'section-control', align: 'left', yOffset: 32, status: 'SECURE', pulseTimer: 0 },
  { id: 'newsletter-mcp', label: 'MCP CONNECTOR', sectionId: 'section-newsletter', align: 'right', yOffset: 96, status: 'LISTENING', pulseTimer: 0 },
  { id: 'footer-sync', label: 'SYSTEM STATE', sectionId: 'section-footer', align: 'left', yOffset: 32, status: 'SYNCHRONIZED', pulseTimer: 0 }
];

export function PremiumPixelBackground() {
  const { resolvedTheme } = useTheme();
  const isDarkRef = useRef(resolvedTheme === 'dark');
  useEffect(() => {
    isDarkRef.current = resolvedTheme === 'dark';
  }, [resolvedTheme]);

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const [inViewport, setInViewport] = useState(true);
  const [accentHSL, setAccentHSL] = useState({ h: 221, s: 83, l: 53 });
  const accentHSLRef = useRef({ h: 221, s: 83, l: 53 });

  // References for rendering logic (refs used for perfect 60fps)
  const pathsRef = useRef<CircuitPath[]>([]);
  const packetsRef = useRef<Packet[]>([]);
  const lastMasterSpawnRef = useRef<number>(0);
  const nodeStatesRef = useRef<SubSystemNode[]>(SUBSYSTEM_NODES);
  const sectionPositionsRef = useRef<Record<string, number>>({});
  const sectionHeightsRef = useRef<Record<string, number>>({});
  const exclusionZonesRef = useRef<ExclusionZone[]>([]);
  const pulseWavesRef = useRef<{ y: number; speed: number; alpha: number }[]>([]);
  
  // Track hover status per section
  const hoveredSectionRef = useRef<string | null>(null);

  // Track dynamic portrait centerpiece coordinates
  const portraitCenterRef = useRef({ x: 0, y: 0 });

  // Track page size
  const documentHeightRef = useRef(0);

  // Measure sections on the homepage to update routing y-coordinates
  const measureSections = useCallback(() => {
    try {
      const heights: Record<string, number> = {};
      const GRID = 32;
      let docHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
      documentHeightRef.current = docHeight;

      // Find dynamic center of portrait centerpiece
      const portraitEl = document.getElementById('hero-portrait-container');
      if (portraitEl) {
        const rect = portraitEl.getBoundingClientRect();
        const absoluteX = rect.left + rect.width / 2;
        const absoluteY = rect.top + window.scrollY + rect.height * 0.42;
        // Snap to grid
        portraitCenterRef.current = {
          x: Math.round(absoluteX / GRID) * GRID,
          y: Math.round(absoluteY / GRID) * GRID
        };
      } else {
        portraitCenterRef.current = {
          x: Math.round((window.innerWidth * 0.58) / GRID) * GRID,
          y: Math.round(450 / GRID) * GRID
        };
      }

      // Hero section Y defaults to 250
      const hero = document.querySelector('section');
      heights['section-hero'] = hero ? hero.getBoundingClientRect().top + window.scrollY : 250;

      // Measure rest of sections
      const sectionHeights: Record<string, number> = {};
      SUBSYSTEM_NODES.forEach(node => {
        if (node.sectionId === 'section-hero') return;
        const el = document.getElementById(node.sectionId) || document.querySelector(`[id*="${node.sectionId}"]`);
        if (el) {
          const rect = el.getBoundingClientRect();
          heights[node.sectionId] = rect.top + window.scrollY;
          sectionHeights[node.sectionId] = rect.height;
        } else {
          // Fixed static grid-aligned Y coordinates for pages where these sections do not exist (guarantees locked lines across all routes)
          const fixedY = node.sectionId === 'section-mission' ? 640
                       : node.sectionId === 'section-solutions' ? 1280
                       : node.sectionId === 'section-projects' ? 1920
                       : node.sectionId === 'section-labs' ? 2560
                       : node.sectionId === 'section-journal' ? 3200
                       : node.sectionId === 'section-control' ? 3840
                       : node.sectionId === 'section-newsletter' ? 4480
                       : 5120;
          heights[node.sectionId] = fixedY;
          sectionHeights[node.sectionId] = 400; // static default height fallback
        }
      });

      // Footer
      const footer = document.getElementById('section-footer') || document.querySelector('footer');
      heights['section-footer'] = footer ? footer.getBoundingClientRect().top + window.scrollY : docHeight - 200;
      sectionHeights['section-footer'] = 120;

      sectionPositionsRef.current = heights;
      sectionHeightsRef.current = sectionHeights;

      // Dynamic Exclusion Zones Scanner (Detects absolute locations of headings, cards, and buttons)
      const zones: ExclusionZone[] = [];
      const headings = document.querySelectorAll('h1, h2, h3, h4, .section-title, [class*="title"], [class*="heading"]');
      headings.forEach((el, index) => {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          zones.push({
            id: `heading-${index}`,
            x1: rect.left + window.scrollX,
            y1: rect.top + window.scrollY,
            x2: rect.right + window.scrollX,
            y2: rect.bottom + window.scrollY,
            padding: 24
          });
        }
      });

      const cards = document.querySelectorAll('.group\\/card, [class*="card"], [class*="dashboard"], button, .section-divider');
      cards.forEach((el, index) => {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          zones.push({
            id: `card-${index}`,
            x1: rect.left + window.scrollX,
            y1: rect.top + window.scrollY,
            x2: rect.right + window.scrollX,
            y2: rect.bottom + window.scrollY,
            padding: 16
          });
        }
      });

      exclusionZonesRef.current = zones;
      buildMotherboardCircuits();
    } catch { /* suppress */ }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Build PCB motherboard circuit traces connecting the vertical trunks to sections
  function buildMotherboardCircuits() {
    const W = window.innerWidth;
    const docH = documentHeightRef.current || 4000;
    
    // Snapping everything exactly to the 32px blueprint grid lines!
    const GRID = 32;
    const leftCol = Math.round((W * 0.08) / GRID);
    const gridCols = Math.floor(W / GRID);
    const rightCol = gridCols - leftCol;

    const leftTrunkX = leftCol * GRID;
    const rightTrunkX = rightCol * GRID;
    const centerX = Math.round((W * 0.5) / GRID) * GRID;

    // Start exactly at the bottom of the landing hero section (absolute document position)
    const heroEl = document.getElementById('hero-section-root') || document.querySelector('section');
    let startY = 800;
    if (heroEl) {
      const rect = heroEl.getBoundingClientRect();
      // rect.bottom is viewport-relative; add scrollY to get absolute document Y
      const heroBottomAbsolute = rect.bottom + window.scrollY;
      startY = Math.round(heroBottomAbsolute / GRID) * GRID;
    }

    const paths: CircuitPath[] = [];

    // Left & Right continuous main trunks starting from startY (end of hero page)
    paths.push({
      id: 'left-trunk',
      segments: [{ x1: leftTrunkX, y1: startY, x2: leftTrunkX, y2: Math.round((docH - 100) / GRID) * GRID }],
      length: docH - startY
    });
    paths.push({
      id: 'right-trunk',
      segments: [{ x1: rightTrunkX, y1: startY, x2: rightTrunkX, y2: Math.round((docH - 100) / GRID) * GRID }],
      length: docH - startY
    });

    // Generate branches for each subsystem node (only if below hero page)
    nodeStatesRef.current.forEach((node) => {
      if (node.sectionId === 'section-hero') return;
      const secY = sectionPositionsRef.current[node.sectionId] || 500;
      const targetY = Math.round((secY + node.yOffset) / GRID) * GRID;
      if (targetY < startY) return;
      
      const trunkX = node.align === 'left' ? leftTrunkX : rightTrunkX;
      const nodeX = trunkX + (node.align === 'left' ? GRID * 2 : -GRID * 2);

      // 90 degree bracket connection from trunk -> node snapped to 32px steps
      const segments: CircuitSegment[] = [
        { x1: trunkX, y1: targetY - GRID, x2: trunkX, y2: targetY },
        { x1: trunkX, y1: targetY, x2: nodeX, y2: targetY }
      ];

      paths.push({
        id: `branch-${node.id}`,
        segments,
        length: GRID * 3
      });
    });

    // Special Master Circuit path looping snapped exactly to grid (starting at startY)
    const masterSegments: CircuitSegment[] = [];
    const secPositions = nodeStatesRef.current.map(n => Math.round((sectionPositionsRef.current[n.sectionId] || 500) / GRID) * GRID);
    const secHeights = nodeStatesRef.current.map(n => Math.round((sectionHeightsRef.current[n.sectionId] || 400) / GRID) * GRID);

    const pos2 = secPositions[2] || 1000;
    const pos3 = secPositions[3] || 1500;
    const pos4 = secPositions[4] || 2000;
    const pos5 = secPositions[5] || 2500;
    const pos6 = secPositions[6] || 3000;
    const pos7 = secPositions[7] || 3500;
    const pos8 = secPositions[8] || 4000;

    const h2 = secHeights[2] || 400;
    const h3 = secHeights[3] || 400;
    const h4 = secHeights[4] || 400;
    const h5 = secHeights[5] || 400;
    const h6 = secHeights[6] || 400;
    const h7 = secHeights[7] || 400;

    // Define top and bottom bounds of content box per section (aligned below section header title space)
    const boxTop2 = pos2 + GRID * 3;
    const boxBottom2 = pos2 + h2 - GRID;

    const boxTop3 = pos3 + GRID * 3;
    const boxBottom3 = pos3 + h3 - GRID;

    const boxTop4 = pos4 + GRID * 3;
    const boxBottom4 = pos4 + h4 - GRID;

    const boxTop5 = pos5 + GRID * 3;
    const boxBottom5 = pos5 + h5 - GRID;

    const boxTop6 = pos6 + GRID * 3;
    const boxBottom6 = pos6 + h6 - GRID;

    const boxTop7 = pos7 + GRID * 3;
    const boxBottom7 = pos7 + h7 - GRID;

    // Solutions Box
    masterSegments.push({ x1: leftTrunkX, y1: startY, x2: leftTrunkX, y2: boxTop2 });
    masterSegments.push({ x1: leftTrunkX, y1: boxTop2, x2: rightTrunkX, y2: boxTop2 });
    masterSegments.push({ x1: rightTrunkX, y1: boxTop2, x2: rightTrunkX, y2: boxBottom2 });
    masterSegments.push({ x1: rightTrunkX, y1: boxBottom2, x2: leftTrunkX, y2: boxBottom2 });

    // Projects Box
    masterSegments.push({ x1: leftTrunkX, y1: boxBottom2, x2: leftTrunkX, y2: boxTop3 });
    masterSegments.push({ x1: leftTrunkX, y1: boxTop3, x2: rightTrunkX, y2: boxTop3 });
    masterSegments.push({ x1: rightTrunkX, y1: boxTop3, x2: rightTrunkX, y2: boxBottom3 });
    masterSegments.push({ x1: rightTrunkX, y1: boxBottom3, x2: leftTrunkX, y2: boxBottom3 });

    // R&D Labs Box
    masterSegments.push({ x1: leftTrunkX, y1: boxBottom3, x2: leftTrunkX, y2: boxTop4 });
    masterSegments.push({ x1: leftTrunkX, y1: boxTop4, x2: rightTrunkX, y2: boxTop4 });
    masterSegments.push({ x1: rightTrunkX, y1: boxTop4, x2: rightTrunkX, y2: boxBottom4 });
    masterSegments.push({ x1: rightTrunkX, y1: boxBottom4, x2: leftTrunkX, y2: boxBottom4 });

    // Technical Journal Box
    masterSegments.push({ x1: leftTrunkX, y1: boxBottom4, x2: leftTrunkX, y2: boxTop5 });
    masterSegments.push({ x1: leftTrunkX, y1: boxTop5, x2: rightTrunkX, y2: boxTop5 });
    masterSegments.push({ x1: rightTrunkX, y1: boxTop5, x2: rightTrunkX, y2: boxBottom5 });
    masterSegments.push({ x1: rightTrunkX, y1: boxBottom5, x2: leftTrunkX, y2: boxBottom5 });

    // Mission Control Box
    masterSegments.push({ x1: leftTrunkX, y1: boxBottom5, x2: leftTrunkX, y2: boxTop6 });
    masterSegments.push({ x1: leftTrunkX, y1: boxTop6, x2: rightTrunkX, y2: boxTop6 });
    masterSegments.push({ x1: rightTrunkX, y1: boxTop6, x2: rightTrunkX, y2: boxBottom6 });
    masterSegments.push({ x1: rightTrunkX, y1: boxBottom6, x2: leftTrunkX, y2: boxBottom6 });

    // Newsletter Box
    masterSegments.push({ x1: leftTrunkX, y1: boxBottom6, x2: leftTrunkX, y2: boxTop7 });
    masterSegments.push({ x1: leftTrunkX, y1: boxTop7, x2: rightTrunkX, y2: boxTop7 });
    masterSegments.push({ x1: rightTrunkX, y1: boxTop7, x2: rightTrunkX, y2: boxBottom7 });
    masterSegments.push({ x1: rightTrunkX, y1: boxBottom7, x2: leftTrunkX, y2: boxBottom7 });

    // Footer section
    masterSegments.push({ x1: leftTrunkX, y1: boxBottom7, x2: leftTrunkX, y2: pos8 + GRID });
    masterSegments.push({ x1: leftTrunkX, y1: pos8 + GRID, x2: centerX, y2: pos8 + GRID });

    paths.push({
      id: 'master-data-flow',
      segments: masterSegments,
      length: docH * 2
    });

    pathsRef.current = paths;

    // Initialize packets if empty
    if (packetsRef.current.length === 0) {
      const packets: Packet[] = [];

      // Spawn regular traffic packets (slowed speed & bright solid opacity)
      for (let i = 0; i < 150; i++) {
        const pathIdx = Math.floor(Math.random() * paths.length);
        const segmentIdx = Math.floor(Math.random() * paths[pathIdx].segments.length);
        const category = getRandomCategory();
        const label = getRandomLabel(category);
        
        packets.push({
          pathIndex: pathIdx,
          segmentIndex: segmentIdx,
          progress: Math.random(),
          speed: 0.0012 + Math.random() * 0.0028, // Slowed down from 0.006 - 0.014
          size: 3,
          alpha: 0.8 + Math.random() * 0.2, // Bright visibility baseline
          isMaster: false,
          label,
          category
        });
      }
      packetsRef.current = packets;
    }
  };

  const getRandomCategory = (): Packet['category'] => {
    const roll = Math.random();
    if (roll < 0.3) return 'request';
    if (roll < 0.55) return 'inference';
    if (roll < 0.75) return 'memory';
    if (roll < 0.9) return 'broadcast';
    return 'success';
  };

  const getRandomLabel = (cat: Packet['category'], nodeSection?: string | null): string => {
    // Override labels based on section hovering
    if (nodeSection === 'section-mission') {
      const voiceLabels = ['STT', 'TTS', 'VOICE', 'AUDIO', 'STREAM'];
      return voiceLabels[Math.floor(Math.random() * voiceLabels.length)];
    }
    if (nodeSection === 'section-projects') {
      const projLabels = ['BUILD', 'DEPLOY', 'TEST', 'PROD', 'DONE'];
      return projLabels[Math.floor(Math.random() * projLabels.length)];
    }
    if (nodeSection === 'section-labs') {
      const labLabels = ['RESEARCH', 'HYPOTHESIS', 'RESULT', 'EXP', 'MATH'];
      return labLabels[Math.floor(Math.random() * labLabels.length)];
    }
    if (nodeSection === 'section-journal') {
      const journalLabels = ['POST', 'ARTICLE', 'JOURNAL', 'WRITE', 'ARCHIVE'];
      return journalLabels[Math.floor(Math.random() * journalLabels.length)];
    }

    const labels = PACKET_LABES[cat];
    return labels[Math.floor(Math.random() * labels.length)];
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Viewport observer
    const observer = new IntersectionObserver(([entry]) => {
      setInViewport(entry.isIntersecting);
    }, { threshold: 0.02 });

    if (containerRef.current) observer.observe(containerRef.current);

    // Initial setup
    measureSections();

    // Event hooks
    const handleScroll = () => {
      // Keep background lines completely static during scroll to prevent jumps
    };

    const handleResize = () => {
      const W = window.innerWidth;
      const H = window.innerHeight;
      canvas.width = W;
      canvas.height = H;
      measureSections();
    };

    // Hover trackers for interactive node redirection
    const handleMouseMove = (e: MouseEvent) => {
      const y = e.pageY;
      const docH = documentHeightRef.current || 4000;
      
      // Determine what section the cursor is currently in
      const ratios = {
        'section-mission': 0.15,
        'section-solutions': 0.3,
        'section-projects': 0.48,
        'section-labs': 0.62,
        'section-journal': 0.72,
        'section-control': 0.80,
        'section-newsletter': 0.88
      };

      let activeSection = null;
      for (const [sec, ratio] of Object.entries(ratios)) {
        if (Math.abs(y / docH - ratio) < 0.08) {
          activeSection = sec;
          break;
        }
      }
      hoveredSectionRef.current = activeSection;
    };

    // Listen to custom hero pulse events to trigger circuit wave highlights
    const handleHeroPulse = (e: Event) => {
      // Emit pulse wave moving down the motherboard trunk lines
      pulseWavesRef.current.push({
        y: portraitCenterRef.current.y || 300,
        speed: 18.0,
        alpha: 1.0
      });

      // Flash active processor node
      const nodes = nodeStatesRef.current;
      if (nodes[0]) {
        nodes[0].pulseTimer = 40;
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleResize);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('hero-pulse', handleHeroPulse);

    // Animation Loop
    let animationFrameId: number;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const render = () => {
      animationFrameId = requestAnimationFrame(render);
      
      if (!inViewport || reducedMotion) return;

      const W = window.innerWidth;
      const H = window.innerHeight;

      // Adjust canvas dimensions inline to match bounding rect exactly with Device Pixel Ratio (DPR)
      const dpr = window.devicePixelRatio || 1;
      if (canvas.width !== W * dpr || canvas.height !== H * dpr) {
        canvas.width = W * dpr;
        canvas.height = H * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0); // Reset scale and apply dpr transform
      }

      ctx.clearRect(0, 0, W, H);

      // ─── 5-Second Master Flow Packet Spawner ───
      const now = Date.now();
      if (now - lastMasterSpawnRef.current >= 5000) {
        if (lastMasterSpawnRef.current === 0) {
          lastMasterSpawnRef.current = now - 3500; // Spawn first packet in 1.5 seconds
        } else {
          lastMasterSpawnRef.current = now;
          const masterPathIdx = pathsRef.current.findIndex(p => p.id === 'master-data-flow');
          if (masterPathIdx !== -1) {
            packetsRef.current.push({
              pathIndex: masterPathIdx,
              segmentIndex: 0,
              progress: 0,
              speed: 0.0016, // Snaking pace
              size: 5.5,
              alpha: 1.0,
              isMaster: true,
              label: 'PNJ-MASTER',
              category: 'broadcast',
              colorOverride: '#FFFFFF'
            });
          }
        }
      }
      
      const scrollY = window.scrollY;
      const isDark = isDarkRef.current;

      // ─── Color Sync (Read directly from document style properties) ────
      let activeH = 221;
      let activeS = 83;
      let activeL = 53;

      try {
        const rootStyles = getComputedStyle(document.documentElement);
        const primaryVal = rootStyles.getPropertyValue('--primary').trim();
        if (primaryVal) {
          const parts = primaryVal.split(/\s+/);
          if (parts.length >= 3) {
            activeH = parseFloat(parts[0]);
            activeS = parseFloat(parts[1].replace('%', ''));
            activeL = parseFloat(parts[2].replace('%', ''));
          }
        }
      } catch { /* fallback */ }

      // Update state when color changes (throttled to avoid loop re-renders)
      if (activeH !== accentHSLRef.current.h || activeS !== accentHSLRef.current.s || activeL !== accentHSLRef.current.l) {
        accentHSLRef.current = { h: activeH, s: activeS, l: activeL };
        setAccentHSL({ h: activeH, s: activeS, l: activeL });
      }

      const accentColor = `hsl(${activeH}, ${activeS}%, ${activeL}%)`;
      const accentColorGlow = `hsla(${activeH}, ${activeS}%, ${activeL}%, 0.25)`;

      // ─── Update waves ───────────────────────────────────────────────────
      const waves = pulseWavesRef.current;
      for (let i = waves.length - 1; i >= 0; i--) {
        const w = waves[i];
        w.y += w.speed;
        w.alpha -= 0.003;
        
        // Pulse sections & nodes as wave passes
        nodeStatesRef.current.forEach(node => {
          const secY = sectionPositionsRef.current[node.sectionId] || 0;
          const targetY = secY + node.yOffset;
          if (Math.abs(w.y - targetY) < 30 && node.pulseTimer <= 0) {
            node.pulseTimer = 45; // trigger pulse
          }
        });

        if (w.alpha <= 0 || w.y > documentHeightRef.current) {
          waves.splice(i, 1);
        }
      }

      // ─── Draw Motherboard Circuits (With Segment-by-Segment Layout-Aware Opacity) ───
      pathsRef.current.forEach(path => {
        const isMaster = path.id === 'master-data-flow';
        const baseOpacity = isMaster ? 0.36 : 0.18;

        path.segments.forEach(seg => {
          // Absolute Y to screen-space Y
          const y1 = seg.y1 - scrollY;
          const y2 = seg.y2 - scrollY;

          // Cull offscreen lines to preserve CPU usage
          if (Math.max(y1, y2) < -100 || Math.min(y1, y2) > H + 100) return;

          // Calculate overlap opacity multiplier
          const multiplier = getSegmentOpacityMultiplier(seg.x1, seg.y1, seg.x2, seg.y2, exclusionZonesRef.current);
          const finalOpacity = baseOpacity * multiplier;

          ctx.beginPath();
          ctx.moveTo(seg.x1, y1);
          ctx.lineTo(seg.x2, y2);

          // Make traces clearly visible
          ctx.strokeStyle = isDark 
            ? `hsla(${activeH}, ${activeS}%, ${activeL}%, ${finalOpacity})` 
            : `rgba(148, 163, 184, ${finalOpacity * 0.85})`;
          ctx.lineWidth = isMaster ? 2.5 : 1.8;
          ctx.stroke();
        });

        // Overlay glowing pulse waves traveling down paths
        waves.forEach(w => {
          path.segments.forEach(seg => {
            const minY = Math.min(seg.y1, seg.y2);
            const maxY = Math.max(seg.y1, seg.y2);
            
            // If wave coordinates are within line range
            if (w.y >= minY && w.y <= maxY) {
              // Draw small highlighted sub-segment
              ctx.beginPath();
              ctx.moveTo(seg.x1, w.y - 40 - scrollY);
              ctx.lineTo(seg.x2, w.y + 40 - scrollY);
              ctx.strokeStyle = accentColor;
              ctx.globalAlpha = w.alpha * 0.7;
              ctx.lineWidth = 2.0;
              ctx.stroke();
              ctx.globalAlpha = 1.0;
            }
          });
        });
      });

      // ─── Draw Surrounding Nodes ─────────────────────────────────────────
      nodeStatesRef.current.forEach(node => {
        const secY = sectionPositionsRef.current[node.sectionId] || 0;
        const nodeY = secY + node.yOffset - scrollY;
        const leftCol = Math.round((W * 0.08) / 32);
        const gridCols = Math.floor(W / 32);
        const rightCol = gridCols - leftCol;
        const trunkX = node.align === 'left' ? leftCol * 32 : rightCol * 32;
        const nodeX = node.align === 'left' ? trunkX + 64 : trunkX - 64;

        if (nodeY < -50 || nodeY > H + 50) return;

        // Decrease pulse timer
        if (node.pulseTimer > 0) node.pulseTimer--;

        // Draw micro node circuit board point
        ctx.save();
        ctx.translate(nodeX, nodeY);

        const isPulsing = node.pulseTimer > 0;
        const alpha = isPulsing ? 0.9 : 0.4;
        const scale = isPulsing ? 1.4 : 1.0;

        // Draw square node marker
        ctx.fillStyle = accentColor;
        ctx.globalAlpha = alpha;
        
        ctx.shadowColor = accentColor;
        ctx.shadowBlur = isPulsing ? 10 : 4;

        ctx.fillRect(-3 * scale, -3 * scale, 6 * scale, 6 * scale);

        // Subsystem details & text label
        ctx.fillStyle = isDark ? '#E2E8F0' : '#1E293B'; 
        ctx.globalAlpha = 0.95;
        ctx.font = 'bold 8.5px monospace';
        const textOffset = node.align === 'left' ? 10 : -10;
        ctx.textAlign = node.align === 'left' ? 'left' : 'right';
        ctx.fillText(node.label, textOffset, -2);
        ctx.fillText(node.status, textOffset, 6);

        ctx.restore();
      });

      // ─── Draw & Update Data Packets (With Monospace Telemetry Labels) ────
      const packets = packetsRef.current;
      packets.forEach(p => {
        const path = pathsRef.current[p.pathIndex];
        if (!path || path.segments.length === 0) return;

        // Update progress
        p.progress += p.speed;
        if (p.progress >= 1.0) {
          p.progress = 0;
          p.segmentIndex = (p.segmentIndex + 1) % path.segments.length;
          
          // Randomly trigger packet error loss (2% chance)
          if (!p.isMaster && Math.random() < 0.02) {
            p.category = 'error';
            p.label = getRandomLabel('error');
          } else if (p.category === 'error') {
            // Recover as retry
            p.category = 'retry';
            p.label = getRandomLabel('retry');
          } else {
            // Cycle new label based on current section hover override
            p.label = getRandomLabel(p.category, hoveredSectionRef.current);
          }
        }

        const seg = path.segments[p.segmentIndex];
        if (!seg) return;

        // Interpolate packet position inside current line segment
        const px = seg.x1 + (seg.x2 - seg.x1) * p.progress;
        const py = seg.y1 + (seg.y2 - seg.y1) * p.progress;

        const screenY = py - scrollY;

        // Draw only if visible in viewport
        if (screenY < -20 || screenY > H + 20) return;

        // Map background packet color strictly to the premium 3-color design system
        let h = activeH;
        let s = activeS;
        let l = isDark ? activeL : (activeL - 10);

        if (p.category === 'error' || p.category === 'retry') {
          // Engineering Red
          h = 358;
          s = 76;
          l = isDark ? 59 : 45;
        } else if (p.category === 'broadcast') {
          // Muted Slate
          h = 215;
          s = 16;
          l = isDark ? 65 : 45;
        } else {
          // Dynamic Sync Color (Electric Blue default, transitions to hovered accent color)
          h = activeH;
          s = activeS;
          l = isDark ? activeL : (activeL - 10);
        }

        let packetColor = `hsla(${h}, ${s}%, ${l}%, `;

        // Adjust alpha based on wave proximity (min baseline 0.55 for high visibility)
        let alpha = Math.max(0.55, p.alpha);
        let size = p.size;
        
        waves.forEach(w => {
          if (Math.abs(w.y - py) < 100) {
            alpha = Math.min(1.0, alpha + 0.35);
            size *= 1.4;
          }
        });

        // ─── If packet enters footer, override label with system states ───
        const isFooterPath = path.id.includes('branch-footer-sync') || path.id.includes('footer');
        let labelText = p.label;
        if (isFooterPath && !p.isMaster) {
          labelText = FOOTER_STATUSES[p.pathIndex % FOOTER_STATUSES.length];
          // Default footer path packets to Electric Blue
          h = 217; s = 91; l = isDark ? 65 : 45;
          packetColor = `hsla(${h}, ${s}%, ${l}%, `;
        }

        // Calculate layout-aware packet dimming inside exclusion zones
        const packetMultiplier = getPacketOpacityMultiplier(px, py, exclusionZonesRef.current);
        const finalAlpha = alpha * packetMultiplier;

        ctx.save();
        ctx.globalAlpha = finalAlpha;

        // Draw square node lead dot
        ctx.fillStyle = p.colorOverride || `${packetColor}1.0)`;
        ctx.shadowColor = p.colorOverride || `${packetColor}1.0)`;
        ctx.shadowBlur = p.isMaster ? 10 : 4;
        ctx.fillRect(px - size / 2, screenY - size / 2, size, size);

        // Draw small monospace text next to packet dot (using a clean terminal green color for all)
        ctx.fillStyle = isDark ? '#22C55E' : '#15803D';
        ctx.font = 'bold 9.5px monospace';
        ctx.shadowBlur = 0; // Disable text shadow to preserve performance
        ctx.fillText(labelText, px + 7, screenY + 3.0);

        ctx.restore();
      });

      ctx.globalAlpha = 1.0;
      ctx.shadowBlur = 0;
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
      observer.disconnect();
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('hero-pulse', handleHeroPulse);
    };
  }, [inViewport, measureSections]);

  return (
    <div 
      ref={containerRef}
      className="fixed inset-0 w-full h-full pointer-events-none z-15 overflow-hidden"
    >
      {/* Site-wide engineering grid background (works in Light and Dark Mode) */}
      <div 
        className="absolute inset-0 bg-left-top"
        style={{
          backgroundImage: `
            linear-gradient(to right, hsla(${accentHSL.h}, ${accentHSL.s}%, ${accentHSL.l}%, 0.055) 1px, transparent 1px),
            linear-gradient(to bottom, hsla(${accentHSL.h}, ${accentHSL.s}%, ${accentHSL.l}%, 0.055) 1px, transparent 1px)
          `,
          backgroundSize: '32px 32px',
          maskImage: 'radial-gradient(ellipse at center, black 65%, transparent 100%)',
          WebkitMaskImage: 'radial-gradient(ellipse at center, black 65%, transparent 100%)'
        }}
      />
      <canvas 
        ref={canvasRef}
        className="absolute inset-0 w-full h-full pointer-events-none"
      />
    </div>
  );
}
