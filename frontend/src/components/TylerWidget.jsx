import React, { useEffect, useState } from 'react';

export default function TylerWidget({ userId, updateTrigger }) {
  const [insight, setInsight] = useState("Hello. I'm Tyler, your curator. Start logging entries to let me get to know you.");
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!userId) return;
    
    setLoading(true);
    fetch(`http://127.0.0.1:8000/api/tyler/insights/${userId}`)
      .then(res => res.json())
      .then(data => {
        if (data.weekly_insight) {
          setInsight(data.weekly_insight);
        }
        if (data.profile) {
          setProfile(data.profile);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching Tyler insights:", err);
        setLoading(false);
      });
  }, [userId, updateTrigger]);

  return (
    <div className="tyler-widget-container glass-panel fade-in-section">
      <div className="tyler-avatar-container">
        {/* Generative Siri/Gemini Style Breathing Plasma Orb */}
        <div className="tyler-orb-wrapper">
          <svg viewBox="0 0 100 100" className="tyler-svg-orb">
            <defs>
              <radialGradient id="g1" cx="30%" cy="30%" r="70%">
                <stop offset="0%" stopColor="#c084fc" stopOpacity="0.8" />
                <stop offset="50%" stopColor="#818cf8" stopOpacity="0.4" />
                <stop offset="100%" stopColor="#1e1b4b" stopOpacity="0" />
              </radialGradient>
              <radialGradient id="g2" cx="70%" cy="60%" r="60%">
                <stop offset="0%" stopColor="#34d399" stopOpacity="0.7" />
                <stop offset="60%" stopColor="#6366f1" stopOpacity="0.3" />
                <stop offset="100%" stopColor="#0c0a0f" stopOpacity="0" />
              </radialGradient>
              <filter id="glow-blur">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" />
              </filter>
            </defs>
            
            <g filter="url(#glow-blur)">
              {/* Outer plasma background */}
              <circle cx="50" cy="50" r="32" fill="url(#g1)" className="orb-layer layer-1" />
              {/* Inner shifting gradient */}
              <circle cx="48" cy="52" r="26" fill="url(#g2)" className="orb-layer layer-2" />
              {/* Center core pulse */}
              <circle cx="52" cy="48" r="18" fill="#a78bfa" opacity="0.3" className="orb-layer layer-3" />
            </g>
          </svg>
          <style>{`
            .tyler-orb-wrapper {
              position: relative;
              width: 76px;
              height: 76px;
            }
            .tyler-svg-orb {
              width: 100%;
              height: 100%;
              overflow: visible;
            }
            .orb-layer {
              transform-origin: 50px 50px;
              mix-blend-mode: screen;
            }
            .layer-1 {
              animation: orb-spin 18s infinite linear, orb-scale-1 6s infinite alternate ease-in-out;
            }
            .layer-2 {
              animation: orb-spin-reverse 12s infinite linear, orb-scale-2 4s infinite alternate ease-in-out;
            }
            .layer-3 {
              animation: orb-pulse 2.5s infinite alternate ease-in-out;
            }
            @keyframes orb-spin {
              from { transform: rotate(0deg); }
              to { transform: rotate(360deg); }
            }
            @keyframes orb-spin-reverse {
              from { transform: rotate(360deg); }
              to { transform: rotate(0deg); }
            }
            @keyframes orb-scale-1 {
              0% { transform: scale(0.9); }
              100% { transform: scale(1.12); }
            }
            @keyframes orb-scale-2 {
              0% { transform: scale(1.15) translate(-2px, 1px); }
              100% { transform: scale(0.85) translate(2px, -1px); }
            }
            @keyframes orb-pulse {
              0% { transform: scale(0.93); opacity: 0.2; }
              100% { transform: scale(1.07); opacity: 0.45; }
            }
          `}</style>
        </div>
        <span className="tyler-name">Tyler</span>
      </div>
      
      <div className="tyler-speech-bubble">
        <h3 className="tyler-greeting">
          {loading ? "Observing your tastes..." : "My latest observations:"}
        </h3>
        <p className="tyler-insight" style={{ whiteSpace: 'pre-line' }}>
          {insight}
        </p>
      </div>
    </div>
  );
}
