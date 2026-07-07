import React from 'react';

export default function PosterDetailModal({ item, userLog, type, onClose, onEditLog }) {
  if (!item) return null;

  const rating = userLog?.rating ?? null;
  const review = userLog?.review ?? null;
  const mechanics = userLog?.favorite_mechanics ?? [];
  const status = userLog?.status ?? null;

  // Build "liked parts" tags for movies from review keywords / manual sections
  const movieHighlightTags = review
    ? (() => {
        const text = review.toLowerCase();
        const tags = [];
        if (/cinematograph|visuals?|shot|lighting|colour|color/.test(text)) tags.push('Cinematography');
        if (/music|score|soundtrack|composer|ost/.test(text)) tags.push('Soundtrack');
        if (/story|narrative|plot|writing|script/.test(text)) tags.push('Story');
        if (/act|perform|character|cast/.test(text)) tags.push('Performances');
        if (/direct|pacing|tension/.test(text)) tags.push('Direction');
        if (/design|world|set|production/.test(text)) tags.push('Production Design');
        return tags;
      })()
    : [];

  const ratingStars = rating ? Math.round((rating / 10) * 5) : 0;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="detail-mini-modal glass-panel"
        onClick={e => e.stopPropagation()}
      >
        {/* Close */}
        <button className="close-btn detail-close" onClick={onClose}>×</button>

        {/* Hero */}
        <div className="detail-mini-hero">
          <div className="detail-mini-poster-wrap">
            <img
              src={item.cover_image || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=400&q=80'}
              alt={item.title}
              className="detail-mini-poster"
            />
            {/* Glow blob behind poster */}
            <div className="detail-mini-poster-glow" />
          </div>

          <div className="detail-mini-info">
            <div className="detail-mini-type-label">
              {type === 'game' ? '🎮 Game' : '🎬 Film'}
              {status && <span className={`detail-mini-status ${status}`}>{status}</span>}
            </div>
            <h2 className="detail-mini-title">{item.title}</h2>
            <div className="detail-mini-meta">
              {type === 'game'
                ? <><span>{item.developer}</span> · <span>{item.publisher}</span></>
                : <><span>{item.director}</span> · <span>{item.studio}</span></>
              }
            </div>
            <div className="detail-mini-meta" style={{ marginTop: '0.25rem' }}>
              {item.release_date && <span>{item.release_date}</span>}
              {(item.genre || []).length > 0 && <span> · {(item.genre || []).join(', ')}</span>}
            </div>

            {/* Rating */}
            <div className="detail-mini-rating-block">
              {rating ? (
                <>
                  <div className="detail-rating-stars">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <span key={i} className={`rating-star ${i < ratingStars ? 'filled' : ''}`}>★</span>
                    ))}
                  </div>
                  <div className="detail-rating-number">
                    <span className="detail-rating-val">{rating}</span>
                    <span className="detail-rating-max">/10</span>
                  </div>
                </>
              ) : (
                <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic' }}>
                  Not rated yet
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Liked Parts */}
        {(mechanics.length > 0 || movieHighlightTags.length > 0 || review) && (
          <div className="detail-mini-liked">
            <div className="detail-mini-section-label">What I liked</div>

            {/* Mechanics tags (games) */}
            {mechanics.length > 0 && (
              <div className="detail-mini-tags">
                {mechanics.map(m => (
                  <span key={m} className="detail-tag game-tag">{m}</span>
                ))}
              </div>
            )}

            {/* Auto-detected movie highlight tags */}
            {movieHighlightTags.length > 0 && (
              <div className="detail-mini-tags">
                {movieHighlightTags.map(t => (
                  <span key={t} className="detail-tag movie-tag">{t}</span>
                ))}
              </div>
            )}

            {/* Review text */}
            {review && (
              <blockquote className="detail-mini-review">
                "{review}"
              </blockquote>
            )}
          </div>
        )}

        {/* Actions */}
        <div className="detail-mini-actions">
          <button
            className="btn btn-primary"
            style={{ fontSize: '0.88rem', padding: '0.6rem 1.25rem' }}
            onClick={() => { onClose(); onEditLog(item); }}
          >
            {rating ? 'Edit Log' : 'Log & Rate'}
          </button>
          <button
            className="btn btn-secondary"
            style={{ fontSize: '0.88rem', padding: '0.6rem 1.25rem' }}
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
