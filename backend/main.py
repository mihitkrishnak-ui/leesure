import os
import datetime
import hashlib
from fastapi import FastAPI, Depends, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional

from models import Base, User, Game, Movie, UserGame, UserMovie, Creator, AIMemory, AIInsight
from agent import TylerAgent

DATABASE_URL = "sqlite:///./leesure.db"

# Create engine & metadata
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Make sure tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="leesure! API", description="AI-powered Entertainment Tracker Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local testing, allow Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize Tyler Agent
tyler = TylerAgent()

# Helper for passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        parts = hashed_password.split("$")
        if len(parts) != 4:
            return False
        _, iterations, salt, key_hex = parts
        dk = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), salt.encode(), int(iterations))
        return dk.hex() == key_hex
    except Exception:
        return False

def hash_password(password: str) -> str:
    salt = "leesure_salt"
    iterations = 100000
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
    return f"pbkdf2_sha256${iterations}${salt}${dk.hex()}"


# --- AUTH ENDPOINTS ---

@app.post("/api/auth/register")
def register(username: str = Body(..., embed=True), password: str = Body(..., embed=True), db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(username=username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(
        username=username,
        password_hash=hash_password(password),
        profile_cosmetics=["Default Violet Glow", "Minimalist Gray"]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize AI Memory for user
    ai_mem = AIMemory(user_id=new_user.id, profile_json={})
    db.add(ai_mem)
    db.commit()

    return {"user_id": new_user.id, "username": new_user.username, "token": f"token_{new_user.id}"}

@app.post("/api/auth/login")
def login(username: str = Body(..., embed=True), password: str = Body(..., embed=True), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return {"user_id": user.id, "username": user.username, "token": f"token_{user.id}"}


# --- CATALOG ENDPOINTS ---

@app.get("/api/games")
def get_games(db: Session = Depends(get_db)):
    return db.query(Game).all()

@app.get("/api/movies")
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@app.get("/api/games/{game_id}")
def get_game_detail(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter_by(id=game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Format and join creators list
    creators = db.query(Creator).filter_by(game_id=game_id).all()
    
    return {
        "game": game,
        "creators": creators
    }

@app.get("/api/movies/{movie_id}")
def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter_by(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


# --- USER TRACKING/LOGS ENDPOINTS ---

@app.get("/api/user/games/{user_id}")
def get_user_games(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(UserGame).filter_by(user_id=user_id).all()
    result = []
    for log in logs:
        game = db.query(Game).filter_by(id=log.game_id).first()
        if game:
            result.append({
                "id": log.id,
                "game_id": log.game_id,
                "title": game.title,
                "cover_image": game.cover_image,
                "developer": game.developer,
                "genre": game.genre,
                "status": log.status,
                "rating": log.rating,
                "review": log.review,
                "hours_played": log.hours_played,
                "completion_percentage": log.completion_percentage,
                "favorite_mechanics": log.favorite_mechanics,
                "favorite_characters": log.favorite_characters,
                "completed_at": log.completed_at
            })
    return result

@app.post("/api/user/games/{user_id}")
def log_user_game(
    user_id: int,
    game_id: int = Body(...),
    status: str = Body("wishlist"),
    rating: Optional[float] = Body(None),
    review: Optional[str] = Body(None),
    hours_played: float = Body(0.0),
    completion_percentage: int = Body(0),
    favorite_mechanics: List[str] = Body([]),
    favorite_characters: List[str] = Body([]),
    db: Session = Depends(get_db)
):
    log = db.query(UserGame).filter_by(user_id=user_id, game_id=game_id).first()
    
    completed_at = None
    if status == "completed":
        completed_at = datetime.datetime.utcnow()

    if log:
        log.status = status
        log.rating = rating
        log.review = review
        log.hours_played = hours_played
        log.completion_percentage = completion_percentage
        log.favorite_mechanics = favorite_mechanics
        log.favorite_characters = favorite_characters
        if completed_at:
            log.completed_at = completed_at
    else:
        log = UserGame(
            user_id=user_id,
            game_id=game_id,
            status=status,
            rating=rating,
            review=review,
            hours_played=hours_played,
            completion_percentage=completion_percentage,
            favorite_mechanics=favorite_mechanics,
            favorite_characters=favorite_characters,
            completed_at=completed_at
        )
        db.add(log)
    
    db.commit()

    # Silent observation: Update Tyler's memory & progression
    tyler.update_user_profile(user_id, db)
    tyler.generate_weekly_insights(user_id, db)

    return {"status": "success", "message": "Game log updated"}


@app.get("/api/user/movies/{user_id}")
def get_user_movies(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(UserMovie).filter_by(user_id=user_id).all()
    result = []
    for log in logs:
        movie = db.query(Movie).filter_by(id=log.movie_id).first()
        if movie:
            result.append({
                "id": log.id,
                "movie_id": log.movie_id,
                "title": movie.title,
                "cover_image": movie.cover_image,
                "director": movie.director,
                "cinematographer": movie.cinematographer,
                "status": log.status,
                "rating": log.rating,
                "review": log.review,
                "watched_at": log.watched_at
            })
    return result

@app.post("/api/user/movies/{user_id}")
def log_user_movie(
    user_id: int,
    movie_id: int = Body(...),
    status: str = Body("watchlist"),
    rating: Optional[float] = Body(None),
    review: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    log = db.query(UserMovie).filter_by(user_id=user_id, movie_id=movie_id).first()
    
    watched_at = None
    if status == "watched":
        watched_at = datetime.datetime.utcnow()

    if log:
        log.status = status
        log.rating = rating
        log.review = review
        if watched_at:
            log.watched_at = watched_at
    else:
        log = UserMovie(
            user_id=user_id,
            movie_id=movie_id,
            status=status,
            rating=rating,
            review=review,
            watched_at=watched_at
        )
        db.add(log)
    
    db.commit()

    # Silent observation: Update Tyler's memory & progression
    tyler.update_user_profile(user_id, db)
    tyler.generate_weekly_insights(user_id, db)

    return {"status": "success", "message": "Movie log updated"}


# --- AI / TYLER ENDPOINTS ---

@app.get("/api/tyler/insights/{user_id}")
def get_tyler_insights(user_id: int, db: Session = Depends(get_db)):
    ai_mem = db.query(AIMemory).filter_by(user_id=user_id).first()
    profile = ai_mem.profile_json if ai_mem else {}
    
    # Fetch latest weekly insight
    insight = db.query(AIInsight).filter_by(user_id=user_id).order_by(AIInsight.id.desc()).first()
    insight_text = insight.insight_text if insight else "Welcome back. Start logging entries to let me get to know you."
    
    return {
        "profile": profile,
        "weekly_insight": insight_text
    }

@app.get("/api/tyler/recommendations/{item_type}/{user_id}")
def get_tyler_recommendations(item_type: str, user_id: int, db: Session = Depends(get_db)):
    if item_type not in ["game", "movie"]:
        raise HTTPException(status_code=400, detail="Invalid recommendation type")
    
    recs = tyler.get_recommendations(user_id, item_type, db)
    return recs


@app.get("/api/profile/{user_id}")
def get_profile_data(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    game_logs = db.query(UserGame).filter_by(user_id=user_id).all()
    movie_logs = db.query(UserMovie).filter_by(user_id=user_id).all()
    
    completed_games = len([g for g in game_logs if g.status == "completed"])
    watched_movies = len([m for m in movie_logs if m.status == "watched"])
    reviews_written = len([g for g in game_logs if g.review]) + len([m for m in movie_logs if m.review])

    # Next Rank requirements
    # Observer -> Explorer -> Collector -> Completionist -> Curator -> Archivist -> Legend
    ranks_order = ["Observer", "Explorer", "Collector", "Completionist", "Curator", "Archivist", "Legend"]
    try:
        current_idx = ranks_order.index(user.rank)
    except ValueError:
        current_idx = 0
        
    next_rank = ranks_order[current_idx + 1] if current_idx < len(ranks_order) - 1 else "Max Rank"
    
    # Calculate level based on XP (every 1000 XP is a level)
    level = (user.xp // 1000) + 1
    xp_in_level = user.xp % 1000

    return {
        "username": user.username,
        "rank": user.rank,
        "next_rank": next_rank,
        "xp": user.xp,
        "level": level,
        "xp_in_level": xp_in_level,
        "completed_games": completed_games,
        "watched_movies": watched_movies,
        "reviews_written": reviews_written,
        "cosmetics": user.profile_cosmetics
    }


# --- GLOBAL SEARCH ENDPOINT ---

@app.get("/api/search")
def global_search(query: str = Query(...), db: Session = Depends(get_db)):
    if len(query) < 2:
        return {"games": [], "movies": []}
    
    # Format query for SQL LIKE search
    search_pattern = f"%{query}%"

    # Search Games
    # We convert JSON columns or check simple text columns
    games = db.query(Game).filter(
        or_(
            Game.title.like(search_pattern),
            Game.developer.like(search_pattern),
            Game.publisher.like(search_pattern),
            Game.description.like(search_pattern)
        )
    ).limit(10).all()

    # Search Movies
    movies = db.query(Movie).filter(
        or_(
            Movie.title.like(search_pattern),
            Movie.director.like(search_pattern),
            Movie.cinematographer.like(search_pattern),
            Movie.music_composer.like(search_pattern),
            Movie.studio.like(search_pattern)
        )
    ).limit(10).all()

    return {
        "games": games,
        "movies": movies
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
