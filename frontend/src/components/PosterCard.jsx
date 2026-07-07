import React, { useEffect, useRef, useState } from 'react';

// Custom Web Audio API Synthesizer for a premium, ambient chime
const playCompletionChime = () => {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    const now = ctx.currentTime;

    // 1. Cinematic sub-bass warm glide
    const subOsc = ctx.createOscillator();
    const subGain = ctx.createGain();
    subOsc.type = 'sine';
    subOsc.frequency.setValueAtTime(110, now); // A2 note
    subOsc.frequency.exponentialRampToValueAtTime(220, now + 0.5); // Glide to A3
    subGain.gain.setValueAtTime(0.4, now);
    subGain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
    subOsc.connect(subGain);
    subGain.connect(ctx.destination);

    // 2. Clear bell chime (minor 7th chord feel)
    const notes = [440, 554, 659, 880]; // A4, C#5, E5, A5
    notes.forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const gainNode = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, now + (idx * 0.06)); // Staggered arpeggio
      
      gainNode.gain.setValueAtTime(0, now);
      gainNode.gain.linearRampToValueAtTime(0.15, now + (idx * 0.06) + 0.05);
      gainNode.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
      
      osc.connect(gainNode);
      gainNode.connect(ctx.destination);
      
      osc.start(now + (idx * 0.06));
      osc.stop(now + 1.8);
    });

    subOsc.start(now);
    subOsc.stop(now + 0.9);
  } catch (e) {
    console.warn("Web Audio API not supported or blocked by browser gesture", e);
  }
};

export default function PosterCard({ item, type, onLogClick }) {
  const canvasRef = useRef(null);
  const [prevStatus, setPrevStatus] = useState(item.status);
  const animationRef = useRef(null);

  useEffect(() => {
    // Detect transitions from not completed -> completed to trigger visual/audio effects
    if (item.status === 'completed' || item.status === 'watched') {
      if (prevStatus && prevStatus !== 'completed' && prevStatus !== 'watched') {
        triggerEffects();
      }
    }
    setPrevStatus(item.status);
  }, [item.status]);

  const triggerEffects = () => {
    // 1. Play synthesized chime
    playCompletionChime();

    // 2. Launch canvas particle physics
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    
    // Scale canvas to match pixel density
    canvas.width = rect.width;
    canvas.height = rect.height;

    const particles = [];
    const particleCount = 45;
    const colors = ['#a78bfa', '#c084fc', '#818cf8', '#6366f1', '#e0e7ff'];

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: canvas.width / 2 + (Math.random() - 0.5) * (canvas.width * 0.6),
        y: canvas.height / 2 + (Math.random() - 0.5) * (canvas.height * 0.6),
        vx: (Math.random() - 0.5) * 4,
        vy: (Math.random() - 0.8) * 5, // Tends upward
        size: Math.random() * 4 + 2,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: 1.0,
        decay: Math.random() * 0.015 + 0.01
      });
    }

    const animateParticles = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      let alive = false;

      particles.forEach(p => {
        if (p.alpha > 0) {
          alive = true;
          p.x += p.vx;
          p.y += p.vy;
          p.vy += 0.05; // tiny gravity
          p.alpha -= p.decay;
          
          ctx.save();
          ctx.globalAlpha = p.alpha;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          // Add a soft glow behind particles
          ctx.shadowBlur = 10;
          ctx.shadowColor = p.color;
          ctx.fill();
          ctx.restore();
        }
      });

      if (alive) {
        animationRef.current = requestAnimationFrame(animateParticles);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    };

    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }
    animateParticles();
  };

  // Determine status mapping
  const isCompleted = item.status === 'completed' || item.status === 'watched';
  const isPlaying = item.status === 'playing';
  const isWishlist = item.status === 'wishlist' || item.status === 'watchlist' || !item.status;

  const cardClasses = `poster-card ${isWishlist ? 'grayscale' : ''} ${isPlaying ? 'playing' : ''} ${isCompleted ? 'completed' : ''}`;

  return (
    <div className="poster-wrapper">
      {/* Visual Canvas Overlay for Achievements */}
      <canvas ref={canvasRef} className="poster-canvas" />

      <div className={cardClasses} onClick={() => onLogClick(item)}>
        <div className="poster-img-container">
          <img 
            src={item.cover_image || "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=600&q=80"} 
            alt={item.title} 
            className="poster-img"
            loading="lazy"
          />
          {item.status && (
            <span className={`status-indicator ${isCompleted ? 'completed' : isPlaying ? 'playing' : 'wishlist'}`}>
              {item.status}
            </span>
          )}
          
          <div className="poster-overlay">
            <div className="poster-details-mini">
              <span className="poster-meta-mini">{type === 'game' ? item.developer : item.director}</span>
              <h4 className="poster-title-mini">{item.title}</h4>
              {item.rating && (
                <div style={{ display: 'flex', gap: '2px', color: '#fbbf24', marginTop: '4px', fontSize: '11px' }}>
                  ★ {item.rating} / 10
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
