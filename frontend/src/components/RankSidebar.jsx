import React from 'react';

// ─── Rank Definitions ────────────────────────────────────────────────────────

// 5-level combined system — linear, 10 items per level
const COMBINED_RANKS = [
  { label: 'Wanderer',    threshold: 0  },
  { label: 'Explorer',    threshold: 10 },
  { label: 'Enthusiast',  threshold: 20 },
  { label: 'Connoisseur', threshold: 30 },
  { label: 'Curator',     threshold: 40 },
];

// 7-level names for games and movies
const GAME_RANK_NAMES  = ['Newcomer', 'Hobbyist', 'Gamer',   'Veteran',  'Champion', 'Master',  'Legend'];
const MOVIE_RANK_NAMES = ['Viewer',   'Cinephile','Critic',  'Analyst',  'Archivist','Curator', 'Auteur'];

// Build 14-segment structure (7 levels × 2 subdivisions, 3 items per sub)
function buildSegments(names, perSub = 3) {
  const segs = [];
  names.forEach((name, li) => {
    ['I', 'II'].forEach((sub, si) => {
      segs.push({
        label:     `${name} ${sub}`,
        name,
        sub,
        threshold: (li * 2 + si) * perSub,
        isFirst:   si === 0,   // first sub — marks the start of a new rank tier
      });
    });
  });
  return segs;
}

// Find the active segment index (highest threshold the count has reached)
function getActiveIdx(segments, count) {
  let idx = -1;
  for (let i = 0; i < segments.length; i++) {
    if (count >= segments[i].threshold) idx = i;
    else break;
  }
  return idx;
}

// ─── Single Vertical Bar ─────────────────────────────────────────────────────

function VerticalBar({ title, count, segments, type }) {
  const activeIdx = getActiveIdx(segments, count);
  const label     = activeIdx >= 0 ? segments[activeIdx].label : '—';

  const maxThreshold = segments[segments.length - 1].threshold;
  const fillPercent = maxThreshold > 0 ? Math.min((count / maxThreshold) * 100, 100) : 0;

  return (
    <div className={`vbar-col ${type}`}>
      <div className="vbar-title">{title}</div>

      <div className="vbar-track-wrapper">
        <div className="vbar-track">
          <div
            className="vbar-fill"
            style={{ height: `${fillPercent}%` }}
          />
          {segments.map((seg, idx) => {
            const percent = maxThreshold > 0 ? (seg.threshold / maxThreshold) * 100 : 0;
            const isReached = count >= seg.threshold;
            return (
              <div
                key={seg.label}
                className={`vbar-tick ${isReached ? 'active' : ''} ${seg.isFirst ? 'level-start' : ''}`}
                style={{ bottom: `${percent}%` }}
                title={`${seg.label} — ${seg.threshold}+ items`}
              />
            );
          })}
        </div>
      </div>

      <div className="vbar-foot">
        <span className="vbar-count">{count}</span>
        <span className="vbar-name">{label}</span>
      </div>
    </div>
  );
}

// ─── Exported Sidebar ─────────────────────────────────────────────────────────
// mode: 'all' | 'games' | 'movies'

export default function RankSidebar({ gamesCount = 0, moviesCount = 0, mode = 'all' }) {
  const gameSegs  = buildSegments(GAME_RANK_NAMES,  3);
  const movieSegs = buildSegments(MOVIE_RANK_NAMES, 3);

  return (
    <aside className="rank-sidebar glass-panel">
      <div className="rank-sidebar-inner">
        {mode === 'all' && (
          <>
            <VerticalBar
              title="Overall"
              count={gamesCount + moviesCount}
              segments={COMBINED_RANKS}
              type="overall"
            />
            <div className="vbar-divider" />
          </>
        )}
        {(mode === 'all' || mode === 'games') && (
          <>
            <VerticalBar
              title="Games"
              count={gamesCount}
              segments={gameSegs}
              type="games"
            />
          </>
        )}
        {mode === 'all' && <div className="vbar-divider" />}
        {(mode === 'all' || mode === 'movies') && (
          <VerticalBar
            title="Movies"
            count={moviesCount}
            segments={movieSegs}
            type="movies"
          />
        )}
      </div>
    </aside>
  );
}
