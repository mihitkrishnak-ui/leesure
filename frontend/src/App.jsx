import React, { useState, useEffect } from 'react';
import TylerWidget from './components/TylerWidget';
import PosterCard from './components/PosterCard';
import RankSidebar from './components/RankSidebar';

const API = 'http://127.0.0.1:8000';

export default function App() {
  const [session, setSession] = useState(null);
  const [activeTab, setActiveTab] = useState('games');
  const [usernameInput, setUsernameInput] = useState('');
  const [passwordInput, setPasswordInput] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [authError, setAuthError] = useState('');

  // Catalog
  const [games, setGames] = useState([]);
  const [movies, setMovies] = useState([]);
  const [userGames, setUserGames] = useState([]);
  const [userMovies, setUserMovies] = useState([]);

  // Tyler recs
  const [gameRecs, setGameRecs] = useState([]);
  const [movieRecs, setMovieRecs] = useState([]);

  // Search
  const [gameSearch, setGameSearch] = useState('');
  const [movieSearch, setMovieSearch] = useState('');

  // Detail modal
  const [selectedItem, setSelectedItem] = useState(null);
  const [modalType, setModalType] = useState(null);
  const [isLogging, setIsLogging] = useState(false);

  // Log form
  const [logStatus, setLogStatus] = useState('wishlist');
  const [logRating, setLogRating] = useState(0);
  const [logReview, setLogReview] = useState('');
  const [logHours, setLogHours] = useState(0);
  const [logCompletion, setLogCompletion] = useState(0);
  const [logMechanics, setLogMechanics] = useState([]);

  // Profile
  const [profileData, setProfileData] = useState(null);
  const [tylerTrigger, setTylerTrigger] = useState(0);

  // Accessibility settings
  const [reducedMotion, setReducedMotion] = useState(false);
  const [fontSize, setFontSize] = useState('medium');
  const [accentColor, setAccentColor] = useState('violet');

  // Restore session
  useEffect(() => {
    const saved = localStorage.getItem('leesure_session');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed?.user_id && typeof parsed.user_id === 'number') {
          setSession(parsed);
        } else {
          // Stale or invalid session — clear it
          localStorage.removeItem('leesure_session');
        }
      } catch { localStorage.removeItem('leesure_session'); }
    }
    const savedA11y = localStorage.getItem('leesure_a11y');
    if (savedA11y) {
      const a = JSON.parse(savedA11y);
      setReducedMotion(a.reducedMotion ?? false);
      setFontSize(a.fontSize ?? 'medium');
      setAccentColor(a.accentColor ?? 'violet');
    }
  }, []);

  // Apply accessibility settings globally
  useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty('--font-size-base', fontSize === 'small' ? '13px' : fontSize === 'large' ? '17px' : '15px');
    const accents = {
      violet: { color: '#a78bfa', glow: 'rgba(167,139,250,0.3)', border: 'rgba(167,139,250,0.15)' },
      amber:  { color: '#fbbf24', glow: 'rgba(251,191,36,0.3)',  border: 'rgba(251,191,36,0.15)'  },
      cyan:   { color: '#22d3ee', glow: 'rgba(34,211,238,0.3)',  border: 'rgba(34,211,238,0.15)'  },
      rose:   { color: '#fb7185', glow: 'rgba(251,113,133,0.3)', border: 'rgba(251,113,133,0.15)' },
    };
    const a = accents[accentColor] || accents.violet;
    root.style.setProperty('--color-violet', a.color);
    root.style.setProperty('--color-violet-glow', a.glow);
    root.style.setProperty('--border-glow', a.border);
    if (reducedMotion) root.style.setProperty('--transition-cinematic', 'none');
    else root.style.setProperty('--transition-cinematic', 'all 0.5s cubic-bezier(0.25, 1, 0.5, 1)');
    localStorage.setItem('leesure_a11y', JSON.stringify({ reducedMotion, fontSize, accentColor }));
  }, [reducedMotion, fontSize, accentColor]);

  // Data fetching
  useEffect(() => {
    if (!session?.user_id) return;
    const safeArr = setter => data => { if (Array.isArray(data)) setter(data); };
    const safeObj = setter => data => { if (data && typeof data === 'object' && !Array.isArray(data)) setter(data); };
    Promise.all([
      fetch(`${API}/api/games`).then(r => r.json()).then(safeArr(setGames)),
      fetch(`${API}/api/movies`).then(r => r.json()).then(safeArr(setMovies)),
      fetch(`${API}/api/user/games/${session.user_id}`).then(r => r.json()).then(safeArr(setUserGames)),
      fetch(`${API}/api/user/movies/${session.user_id}`).then(r => r.json()).then(safeArr(setUserMovies)),
      fetch(`${API}/api/tyler/recommendations/game/${session.user_id}`).then(r => r.json()).then(safeArr(setGameRecs)),
      fetch(`${API}/api/tyler/recommendations/movie/${session.user_id}`).then(r => r.json()).then(safeArr(setMovieRecs)),
      fetch(`${API}/api/profile/${session.user_id}`).then(r => r.json()).then(safeObj(setProfileData)),
    ]).catch(console.error);
  }, [session, tylerTrigger]);

  // Auth
  const handleAuth = (e) => {
    e.preventDefault();
    setAuthError('');
    const endpoint = isRegister ? 'register' : 'login';
    fetch(`${API}/api/auth/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: usernameInput, password: passwordInput })
    })
      .then(r => { if (!r.ok) return r.json().then(d => { throw new Error(d.detail); }); return r.json(); })
      .then(data => { localStorage.setItem('leesure_session', JSON.stringify(data)); setSession(data); })
      .catch(err => setAuthError(err.message));
  };

  const quickDemo = () => {
    fetch(`${API}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'demo', password: 'tyler' })
    })
      .then(r => r.json())
      .then(data => { localStorage.setItem('leesure_session', JSON.stringify(data)); setSession(data); })
      .catch(() => setAuthError('Cannot reach backend. Make sure it is running on port 8000.'));
  };

  const handleLogout = () => {
    localStorage.removeItem('leesure_session');
    setSession(null);
  };

  // Open detail
  const openDetail = (item, type) => {
    setModalType(type);
    setIsLogging(false);
    if (type === 'game') {
      fetch(`${API}/api/games/${item.id}`).then(r => r.json()).then(data => {
        setSelectedItem({ item: data.game, creators: data.creators });
        const log = userGames.find(g => g.game_id === item.id);
        setLogStatus(log?.status || 'wishlist');
        setLogRating(log?.rating || 0);
        setLogReview(log?.review || '');
        setLogHours(log?.hours_played || 0);
        setLogCompletion(log?.completion_percentage || 0);
        setLogMechanics(log?.favorite_mechanics || []);
      });
    } else {
      fetch(`${API}/api/movies/${item.id}`).then(r => r.json()).then(data => {
        setSelectedItem({ item: data });
        const log = userMovies.find(m => m.movie_id === item.id);
        setLogStatus(log?.status || 'watchlist');
        setLogRating(log?.rating || 0);
        setLogReview(log?.review || '');
      });
    }
  };

  // Save log
  const saveLog = () => {
    const endpoint = modalType === 'game' ? 'games' : 'movies';
    const body = {
      ...(modalType === 'game' ? { game_id: selectedItem.item.id } : { movie_id: selectedItem.item.id }),
      status: logStatus,
      rating: logRating > 0 ? logRating : null,
      review: logReview || null,
      ...(modalType === 'game' ? {
        hours_played: parseFloat(logHours) || 0,
        completion_percentage: parseInt(logCompletion) || 0,
        favorite_mechanics: logMechanics,
        favorite_characters: [],
      } : {}),
    };
    fetch(`${API}/api/user/${endpoint}/${session.user_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
      .then(r => r.json())
      .then(() => { setSelectedItem(null); setTylerTrigger(t => t + 1); })
      .catch(console.error);
  };

  const getPosterInfo = (id, type) => {
    if (type === 'game') {
      const l = userGames.find(g => g.game_id === id);
      return l ? { status: l.status, rating: l.rating } : {};
    }
    const l = userMovies.find(m => m.movie_id === id);
    return l ? { status: l.status, rating: l.rating } : {};
  };

  // Filtered lists
  const filteredGames = games.filter(g =>
    g.title.toLowerCase().includes(gameSearch.toLowerCase()) ||
    (g.developer || '').toLowerCase().includes(gameSearch.toLowerCase()) ||
    (g.genre || []).join(' ').toLowerCase().includes(gameSearch.toLowerCase())
  );
  const filteredMovies = movies.filter(m =>
    m.title.toLowerCase().includes(movieSearch.toLowerCase()) ||
    (m.director || '').toLowerCase().includes(movieSearch.toLowerCase()) ||
    (m.cinematographer || '').toLowerCase().includes(movieSearch.toLowerCase())
  );

  // Rank progression thresholds
  const rankOrder = ['Observer', 'Explorer', 'Collector', 'Completionist', 'Curator', 'Archivist', 'Legend'];

  /* ─── LOGIN SCREEN ─── */
  if (!session) {
    return (
      <div className="login-screen">
        <div className="login-card glass-panel fade-in-section">
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <h1 className="brand-logo" style={{ fontSize: '2.8rem' }}>leesure!</h1>
            <p className="brand-sub" style={{ marginTop: '0.25rem' }}>curated by tyler</p>
          </div>
          <p className="login-tagline">
            An AI companion that quietly learns your taste in cinema and games — and remembers forever.
          </p>
          <form onSubmit={handleAuth}>
            <div className="form-group">
              <label className="form-label">Username</label>
              <input type="text" className="form-input" value={usernameInput}
                onChange={e => setUsernameInput(e.target.value)} required />
            </div>
            <div className="form-group">
              <label className="form-label">Password</label>
              <input type="password" className="form-input" value={passwordInput}
                onChange={e => setPasswordInput(e.target.value)} required />
            </div>
            {authError && <p style={{ color: '#f87171', fontSize: '0.85rem', marginBottom: '1rem', textAlign: 'center' }}>{authError}</p>}
            <button type="submit" className="btn btn-primary" style={{ width: '100%', marginBottom: '0.75rem' }}>
              {isRegister ? 'Begin Journey' : 'Step Inside'}
            </button>
          </form>
          <button type="button" className="btn btn-secondary"
            style={{ width: '100%', borderColor: 'rgba(167,139,250,0.3)', marginBottom: '1.25rem' }}
            onClick={quickDemo}>
            🔑 Quick Demo Entry (demo / tyler)
          </button>
          <p className="login-toggle" onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? 'Already have a profile? Sign in' : 'Create a new profile'}
          </p>
        </div>
      </div>
    );
  }

  /* ─── MAIN APP ─── */
  return (
    <div className="app-container">

      {/* ── SIDEBAR ── */}
      <nav className="sidebar-nav">
        <div>
          <div className="brand-section">
            <div>
              <h1 className="brand-logo">leesure!</h1>
              <p className="brand-sub">with tyler</p>
            </div>
          </div>

          <div className="nav-links" style={{ marginTop: '2.5rem' }}>
            <div className={`nav-link ${activeTab === 'games' ? 'active' : ''}`} onClick={() => setActiveTab('games')}>
              <span className="nav-icon-dot" />
              <span>Games</span>
            </div>
            <div className={`nav-link ${activeTab === 'movies' ? 'active' : ''}`} onClick={() => setActiveTab('movies')}>
              <span className="nav-icon-dot" />
              <span>Movies</span>
            </div>
            <div className={`nav-link ${activeTab === 'settings' ? 'active' : ''}`} onClick={() => setActiveTab('settings')}>
              <span className="nav-icon-dot" />
              <span>Settings</span>
            </div>
          </div>
        </div>

        {/* User chip at bottom */}
        <div style={{ padding: '0 0.5rem' }}>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
            Signed in
          </div>
          <div style={{ fontSize: '0.95rem', color: 'var(--text-primary)', marginBottom: '1rem', fontWeight: 500 }}>
            {session.username}
          </div>
          <button className="btn btn-secondary" style={{ width: '100%', padding: '0.5rem', fontSize: '0.85rem' }} onClick={handleLogout}>
            Sign out
          </button>
        </div>
      </nav>

      {/* ── CONTENT ── */}
      <main className="main-content">

        {/* ══ GAMES ══ */}
        {activeTab === 'games' && (
          <div className="fade-in-section dashboard-grid">
            <div className="dashboard-main">
              <TylerWidget userId={session.user_id} updateTrigger={tylerTrigger} />

              {/* Search + filter bar */}
              <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', alignItems: 'center' }}>
                <input
                  type="text"
                  className="form-input"
                  placeholder="Search games, developers, genres…"
                  value={gameSearch}
                  onChange={e => setGameSearch(e.target.value)}
                  style={{ fontSize: '1rem', flex: 1 }}
                />
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', whiteSpace: 'nowrap' }}>
                  {filteredGames.length} titles
                </span>
              </div>

              {/* Tyler's picks */}
              {gameRecs.length > 0 && !gameSearch && (
                <div style={{ marginBottom: '3rem' }}>
                  <h2 className="section-title">Tyler's Picks</h2>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
                    {gameRecs.map(rec => (
                      <div key={`rec-${rec.id}`} className="rec-card glass-panel"
                        onClick={() => openDetail({ id: rec.id }, 'game')}>
                        <img src={rec.cover_image} className="rec-poster" alt="" />
                        <div className="rec-info">
                          <span className="rec-meta">{rec.developer}</span>
                          <h4 className="rec-title">{rec.title}</h4>
                          <p className="rec-reason">{rec.reason}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Full catalog */}
              <h2 className="section-title">{gameSearch ? 'Search Results' : 'All Games'}</h2>
              <div className="posters-container">
                {filteredGames.map(game => (
                  <PosterCard
                    key={`g-${game.id}`}
                    item={{ ...game, ...getPosterInfo(game.id, 'game') }}
                    type="game"
                    onLogClick={item => openDetail(item, 'game')}
                  />
                ))}
                {filteredGames.length === 0 && (
                  <div style={{ gridColumn: '1/-1', textAlign: 'center', color: 'var(--text-muted)', padding: '3rem', fontStyle: 'italic' }}>
                    No games found for "{gameSearch}"
                  </div>
                )}
              </div>
            </div>
            <RankSidebar gamesCount={userGames.length} moviesCount={userMovies.length} />
          </div>
        )}

        {/* ══ MOVIES ══ */}
        {activeTab === 'movies' && (
          <div className="fade-in-section dashboard-grid">
            <div className="dashboard-main">
              <TylerWidget userId={session.user_id} updateTrigger={tylerTrigger} />

              <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', alignItems: 'center' }}>
                <input
                  type="text"
                  className="form-input"
                  placeholder="Search films, directors, cinematographers…"
                  value={movieSearch}
                  onChange={e => setMovieSearch(e.target.value)}
                  style={{ fontSize: '1rem', flex: 1 }}
                />
                <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', whiteSpace: 'nowrap' }}>
                  {filteredMovies.length} films
                </span>
              </div>

              {movieRecs.length > 0 && !movieSearch && (
                <div style={{ marginBottom: '3rem' }}>
                  <h2 className="section-title">Tyler's Picks</h2>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
                    {movieRecs.map(rec => (
                      <div key={`rec-${rec.id}`} className="rec-card glass-panel"
                        onClick={() => openDetail({ id: rec.id }, 'movie')}>
                        <img src={rec.cover_image} className="rec-poster" alt="" />
                        <div className="rec-info">
                          <span className="rec-meta">{rec.director}</span>
                          <h4 className="rec-title">{rec.title}</h4>
                          <p className="rec-reason">{rec.reason}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <h2 className="section-title">{movieSearch ? 'Search Results' : 'All Films'}</h2>
              <div className="posters-container">
                {filteredMovies.map(movie => (
                  <PosterCard
                    key={`m-${movie.id}`}
                    item={{ ...movie, ...getPosterInfo(movie.id, 'movie') }}
                    type="movie"
                    onLogClick={item => openDetail(item, 'movie')}
                  />
                ))}
                {filteredMovies.length === 0 && (
                  <div style={{ gridColumn: '1/-1', textAlign: 'center', color: 'var(--text-muted)', padding: '3rem', fontStyle: 'italic' }}>
                    No films found for "{movieSearch}"
                  </div>
                )}
              </div>
            </div>
            <RankSidebar gamesCount={userGames.length} moviesCount={userMovies.length} />
          </div>
        )}

        {/* ══ SETTINGS ══ */}
        {activeTab === 'settings' && (
          <div className="fade-in-section">
            <h2 className="section-title">Settings</h2>

            {/* ── ACCOUNT ── */}
            <div style={{ marginBottom: '2.5rem' }}>
              <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.15em', color: 'var(--color-violet)', marginBottom: '1rem' }}>
                Account
              </h3>
              <div className="glass-panel" style={{ padding: '2rem', display: 'flex', alignItems: 'center', gap: '2rem' }}>
                {/* Avatar orb */}
                <div style={{
                  width: 72, height: 72, borderRadius: '50%',
                  background: 'radial-gradient(circle, #8b5cf6 0%, #4c1d95 60%, #000 100%)',
                  boxShadow: '0 0 24px rgba(139,92,246,0.4)', flexShrink: 0
                }} />
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '1.4rem', fontWeight: 500, marginBottom: '0.25rem' }}>{session.username}</div>
                  {profileData && (
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                      Rank: <span style={{ color: 'var(--color-violet)' }}>{profileData.rank}</span>
                      {' · '} Level {profileData.level}
                      {' · '} {profileData.xp} XP
                    </div>
                  )}
                </div>
                <button className="btn btn-secondary" style={{ fontSize: '0.85rem' }} onClick={handleLogout}>
                  Sign out
                </button>
              </div>
            </div>

            {/* ── PROGRESSION ── */}
            {profileData && (
              <div style={{ marginBottom: '2.5rem' }}>
                <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.15em', color: 'var(--color-violet)', marginBottom: '1rem' }}>
                  Progression
                </h3>
                <div className="glass-panel" style={{ padding: '2rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem' }}>
                    <div>
                      <div style={{ fontSize: '1.8rem', color: 'var(--color-violet)', fontWeight: 500 }}>{profileData.rank}</div>
                      <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                        Next: {profileData.next_rank}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '1.4rem', fontWeight: 300 }}>{profileData.xp} XP</div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Level {profileData.level}</div>
                    </div>
                  </div>
                  <div className="xp-progress-bar">
                    <div className="xp-fill" style={{ width: `${Math.min((profileData.xp_in_level / 1000) * 100, 100)}%` }} />
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginTop: '2rem' }}>
                    {[
                      { val: profileData.completed_games, lbl: 'Worlds Conquered' },
                      { val: profileData.watched_movies, lbl: 'Films Preserved' },
                      { val: profileData.reviews_written, lbl: 'Reviews Written' },
                    ].map(s => (
                      <div key={s.lbl} style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: '2rem', fontWeight: 300 }}>{s.val}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginTop: '0.2rem' }}>{s.lbl}</div>
                      </div>
                    ))}
                  </div>

                  {/* Rank ladder */}
                  <div style={{ marginTop: '2rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    {rankOrder.map(r => {
                      const reached = rankOrder.indexOf(r) <= rankOrder.indexOf(profileData.rank);
                      return (
                        <div key={r} style={{
                          padding: '0.3rem 0.75rem', borderRadius: '99px', fontSize: '0.75rem',
                          background: reached ? 'rgba(167,139,250,0.12)' : 'transparent',
                          color: reached ? 'var(--color-violet)' : 'var(--text-muted)',
                          border: `1px solid ${reached ? 'rgba(167,139,250,0.3)' : 'rgba(255,255,255,0.05)'}`,
                        }}>
                          {r}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {/* ── COSMETICS ── */}
            {profileData?.cosmetics?.length > 0 && (
              <div style={{ marginBottom: '2.5rem' }}>
                <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.15em', color: 'var(--color-violet)', marginBottom: '1rem' }}>
                  Unlocked Cosmetics
                </h3>
                <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                  {profileData.cosmetics.map(c => (
                    <div key={c} className="glass-panel" style={{ padding: '0.75rem 1.25rem', fontSize: '0.9rem' }}>
                      <span style={{ color: 'var(--color-violet)', marginRight: '0.4rem' }}>✦</span>{c}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* ── APPEARANCE ── */}
            <div style={{ marginBottom: '2.5rem' }}>
              <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.15em', color: 'var(--color-violet)', marginBottom: '1rem' }}>
                Appearance
              </h3>
              <div className="glass-panel" style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
                {/* Accent color */}
                <div>
                  <div className="form-label" style={{ marginBottom: '0.75rem' }}>Accent Color</div>
                  <div style={{ display: 'flex', gap: '0.75rem' }}>
                    {[
                      { id: 'violet', color: '#a78bfa', label: 'Violet' },
                      { id: 'amber',  color: '#fbbf24', label: 'Amber'  },
                      { id: 'cyan',   color: '#22d3ee', label: 'Cyan'   },
                      { id: 'rose',   color: '#fb7185', label: 'Rose'   },
                    ].map(opt => (
                      <button key={opt.id} onClick={() => setAccentColor(opt.id)}
                        style={{
                          width: 36, height: 36, borderRadius: '50%',
                          background: opt.color, border: accentColor === opt.id ? `3px solid white` : '3px solid transparent',
                          cursor: 'pointer', boxShadow: accentColor === opt.id ? `0 0 14px ${opt.color}88` : 'none',
                          transition: 'all 0.2s',
                        }}
                        title={opt.label}
                      />
                    ))}
                  </div>
                </div>

                {/* Font size */}
                <div>
                  <div className="form-label" style={{ marginBottom: '0.75rem' }}>Text Size</div>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    {['small', 'medium', 'large'].map(s => (
                      <button key={s} onClick={() => setFontSize(s)} className={`btn ${fontSize === s ? 'btn-primary' : 'btn-secondary'}`}
                        style={{ padding: '0.4rem 1rem', fontSize: '0.85rem', textTransform: 'capitalize' }}>
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* ── ACCESSIBILITY ── */}
            <div style={{ marginBottom: '2.5rem' }}>
              <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.15em', color: 'var(--color-violet)', marginBottom: '1rem' }}>
                Accessibility
              </h3>
              <div className="glass-panel" style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                {/* Reduced Motion */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 400, marginBottom: '0.15rem' }}>Reduce Motion</div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Disables animations and cinematic transitions</div>
                  </div>
                  <div onClick={() => setReducedMotion(!reducedMotion)} style={{
                    width: 44, height: 24, borderRadius: '99px', cursor: 'pointer', position: 'relative', flexShrink: 0,
                    background: reducedMotion ? 'var(--color-violet)' : 'rgba(255,255,255,0.08)',
                    transition: 'background 0.2s', border: '1px solid rgba(255,255,255,0.1)',
                  }}>
                    <div style={{
                      position: 'absolute', top: 3, left: reducedMotion ? 23 : 3,
                      width: 16, height: 16, borderRadius: '50%', background: 'white',
                      transition: 'left 0.2s', boxShadow: '0 1px 4px rgba(0,0,0,0.4)',
                    }} />
                  </div>
                </div>
              </div>
            </div>

            {/* ── ABOUT TYLER ── */}
            <div>
              <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.15em', color: 'var(--color-violet)', marginBottom: '1rem' }}>
                About Tyler
              </h3>
              <div className="glass-panel" style={{ padding: '2rem' }}>
                <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, fontSize: '0.95rem' }}>
                  Tyler is your personal AI entertainment curator. He silently observes every game and film you log — tracking your
                  favorite developers, directors, cinematographers, composers, and mechanics — and builds a long-term memory of your taste.
                </p>
                <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, fontSize: '0.95rem', marginTop: '1rem' }}>
                  Every recommendation comes with an explanation. Tyler doesn't just say "you might like this" — he tells you exactly why.
                  As you log more entries, Tyler's understanding deepens.
                </p>
                <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(167,139,250,0.05)', borderRadius: '8px', border: '1px solid rgba(167,139,250,0.1)', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  <strong style={{ color: 'var(--text-secondary)' }}>Optional:</strong> Add a <code style={{ color: 'var(--color-violet)' }}>GEMINI_API_KEY</code> or <code style={{ color: 'var(--color-violet)' }}>OPENAI_API_KEY</code> to <code>backend/.env</code> to unlock fully generative, conversational Tyler insights.
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* ══ DETAIL MODAL ══ */}
      {selectedItem && (
        <div className="modal-overlay" onClick={() => setSelectedItem(null)}>
          <div className="modal-content glass-panel" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <div>
                <span style={{ fontSize: '0.72rem', color: 'var(--color-violet)', textTransform: 'uppercase', letterSpacing: '0.15em' }}>
                  {modalType === 'game' ? 'Game' : 'Film'}
                </span>
                <h2 className="modal-title">{selectedItem.item.title}</h2>
              </div>
              <button className="close-btn" onClick={() => setSelectedItem(null)}>×</button>
            </div>

            {/* Hero */}
            <div style={{ display: 'grid', gridTemplateColumns: '140px 1fr', gap: '1.75rem', marginBottom: '2rem' }}>
              <img src={selectedItem.item.cover_image} alt=""
                style={{ width: 140, height: 210, objectFit: 'cover', borderRadius: '8px', boxShadow: '0 8px 24px rgba(0,0,0,0.5)' }} />
              <div>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.65, marginBottom: '1rem' }}>
                  {selectedItem.item.description}
                </p>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.6rem', fontSize: '0.82rem' }}>
                  <div><span style={{ color: 'var(--text-muted)' }}>{modalType === 'game' ? 'Developer' : 'Director'}: </span>
                    {modalType === 'game' ? selectedItem.item.developer : selectedItem.item.director}</div>
                  <div><span style={{ color: 'var(--text-muted)' }}>{modalType === 'game' ? 'Publisher' : 'Studio'}: </span>
                    {modalType === 'game' ? selectedItem.item.publisher : selectedItem.item.studio}</div>
                  <div><span style={{ color: 'var(--text-muted)' }}>Released: </span>{selectedItem.item.release_date}</div>
                  {modalType === 'movie' && <>
                    <div><span style={{ color: 'var(--text-muted)' }}>Cinematographer: </span>{selectedItem.item.cinematographer}</div>
                    <div><span style={{ color: 'var(--text-muted)' }}>Composer: </span>{selectedItem.item.music_composer}</div>
                  </>}
                  <div><span style={{ color: 'var(--text-muted)' }}>Genre: </span>
                    {(selectedItem.item.genre || []).join(', ')}</div>
                </div>
              </div>
            </div>

            {/* Status strip */}
            <div style={{ borderTop: '1px solid var(--border-glass)', paddingTop: '1.5rem' }}>
              {!isLogging ? (
                <>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
                    <div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Your status</div>
                      <div style={{ fontSize: '1rem', textTransform: 'capitalize', marginTop: '0.2rem' }}>
                        {getPosterInfo(selectedItem.item.id, modalType).status || 'Not logged'}
                      </div>
                    </div>
                    <button className="btn btn-primary" onClick={() => setIsLogging(true)}>Log / Update</button>
                  </div>

                  {/* Creators (games only) */}
                  {modalType === 'game' && selectedItem.creators?.length > 0 && (
                    <div style={{ marginBottom: '1.75rem' }}>
                      <div style={{ fontSize: '0.72rem', color: 'var(--color-violet)', textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: '0.75rem' }}>
                        Tyler's Creator Picks
                      </div>
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.6rem' }}>
                        {selectedItem.creators.map(c => (
                          <a key={c.id} href={c.channel_url} target="_blank" rel="noreferrer"
                            className="glass-panel"
                            style={{ padding: '0.65rem 0.85rem', textDecoration: 'none', display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                            <span style={{ fontSize: '0.85rem', color: 'var(--text-primary)' }}>{c.creator_name}</span>
                            <span style={{ fontSize: '0.7rem', color: 'var(--color-amber)', textTransform: 'uppercase' }}>{c.category} · {c.platform}</span>
                          </a>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Trivia */}
                  {((selectedItem.item.interesting_facts || []).length > 0 || (selectedItem.item.trivia || []).length > 0) && (
                    <div>
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: '0.75rem' }}>
                        Trivia
                      </div>
                      <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        {[...(selectedItem.item.interesting_facts || []), ...(selectedItem.item.trivia || [])].map((t, i) => (
                          <li key={i}>{t}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </>
              ) : (
                <>
                  <h3 style={{ fontSize: '1rem', fontWeight: 400, marginBottom: '1.5rem' }}>Log Entry</h3>

                  <div className="form-group">
                    <label className="form-label">Status</label>
                    <select className="form-select" value={logStatus} onChange={e => setLogStatus(e.target.value)}>
                      {modalType === 'game'
                        ? ['wishlist', 'playing', 'completed'].map(s => <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>)
                        : ['watchlist', 'watched'].map(s => <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>)
                      }
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="form-label">Rating (1–10)</label>
                    <div className="rating-selector">
                      {[1,2,3,4,5,6,7,8,9,10].map(n => (
                        <div key={n} className={`rating-dot ${logRating === n ? 'active' : ''}`} onClick={() => setLogRating(n)}>{n}</div>
                      ))}
                    </div>
                  </div>

                  {modalType === 'game' && (
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                      <div className="form-group">
                        <label className="form-label">Hours Played</label>
                        <input type="number" step="0.5" className="form-input" value={logHours} onChange={e => setLogHours(e.target.value)} />
                      </div>
                      <div className="form-group">
                        <label className="form-label">Completion %</label>
                        <input type="number" min="0" max="100" className="form-input" value={logCompletion} onChange={e => setLogCompletion(e.target.value)} />
                      </div>
                    </div>
                  )}

                  {modalType === 'game' && (
                    <div className="form-group">
                      <label className="form-label">Favourite Mechanics</label>
                      <div className="tag-selector">
                        {['Perfect Deflect', 'Dodge Roll', 'Boon Drafting', 'Card Drafting', 'Spell Synergies', 'Open World', 'Stealth'].map(m => (
                          <div key={m} className={`tag-option ${logMechanics.includes(m) ? 'selected' : ''}`}
                            onClick={() => setLogMechanics(prev => prev.includes(m) ? prev.filter(x => x !== m) : [...prev, m])}>
                            {m}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="form-group">
                    <label className="form-label">Review</label>
                    <textarea className="form-textarea" rows="3"
                      placeholder="Capture your thoughts…"
                      value={logReview} onChange={e => setLogReview(e.target.value)} />
                  </div>

                  <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.5rem' }}>
                    <button className="btn btn-primary" onClick={saveLog}>Preserve Memory</button>
                    <button className="btn btn-secondary" onClick={() => setIsLogging(false)}>Cancel</button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
