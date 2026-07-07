import React from 'react';

export default function PersonalLeaderboard({ userItems = [], allItems = [], type = 'game' }) {
  // Merge catalog info with user log data, filter to rated items only
  const ranked = userItems
    .filter(u => (u.rating ?? 0) > 0)
    .map(u => {
      const catalogId = type === 'game' ? u.game_id : u.movie_id;
      const info = allItems.find(i => i.id === catalogId) || {};
      return {
        ...info,
        ...u,
        _id: catalogId,
      };
    })
    .sort((a, b) => (b.rating ?? 0) - (a.rating ?? 0));

  if (ranked.length === 0) {
    return (
      <div className="leaderboard-empty">
        <span>Rate some {type === 'game' ? 'games' : 'films'} to build your personal chart</span>
      </div>
    );
  }

  const getMedalColor = (idx) => {
    if (idx === 0) return '#fbbf24';   // gold
    if (idx === 1) return '#94a3b8';   // silver
    if (idx === 2) return '#b45309';   // bronze
    return 'var(--text-muted)';
  };

  return (
    <div className="leaderboard-panel">
      <h2 className="section-title" style={{ fontSize: '1.1rem', marginBottom: '1.25rem' }}>
        My {type === 'game' ? 'Games' : 'Films'} Chart
      </h2>
      <div className="leaderboard-list">
        {ranked.map((item, idx) => {
          const ratingPct = ((item.rating ?? 0) / 10) * 100;
          return (
            <div key={`lb-${item._id}`} className="leaderboard-row">
              <span className="lb-rank" style={{ color: getMedalColor(idx) }}>
                {idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : `#${idx + 1}`}
              </span>
              <img
                src={item.cover_image || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=120&q=60'}
                alt={item.title}
                className="lb-thumb"
              />
              <div className="lb-info">
                <div className="lb-title">{item.title}</div>
                <div className="lb-sub">
                  {type === 'game' ? item.developer : item.director}
                  {item.status && (
                    <span className={`lb-status-dot ${item.status}`} />
                  )}
                </div>
                <div className="lb-bar-wrap">
                  <div className="lb-bar-track">
                    <div
                      className="lb-bar-fill"
                      style={{ width: `${ratingPct}%` }}
                    />
                  </div>
                  <span className="lb-score">{item.rating}<span style={{ fontSize: '0.65rem', opacity: 0.5 }}>/10</span></span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
