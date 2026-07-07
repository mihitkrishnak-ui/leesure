import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, Text, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    rank = Column(String, default="Observer")  # Observer, Explorer, Collector, Completionist, Curator, Archivist, Legend
    xp = Column(Integer, default=0)
    profile_cosmetics = Column(JSON, default=list) # List of unlocked cosmetic items/themes
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    games = relationship("UserGame", back_populates="user", cascade="all, delete-orphan")
    movies = relationship("UserMovie", back_populates="user", cascade="all, delete-orphan")
    ai_memory = relationship("AIMemory", back_populates="user", uselist=False, cascade="all, delete-orphan")
    insights = relationship("AIInsight", back_populates="user", cascade="all, delete-orphan")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    release_date = Column(String, nullable=True)
    developer = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    genre = Column(JSON, nullable=True)  # List of genres
    platforms = Column(JSON, nullable=True)  # List of platforms
    cover_image = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    screenshots = Column(JSON, default=list)
    trailers = Column(JSON, default=list)  # List of video URLs
    interesting_facts = Column(JSON, default=list)
    news = Column(JSON, default=list)
    community_discussions = Column(JSON, default=list)
    dlc_info = Column(JSON, default=list)
    similar_games = Column(JSON, default=list)  # List of game IDs or titles

    # Relationships
    creators = relationship("Creator", back_populates="game", cascade="all, delete-orphan")
    user_associations = relationship("UserGame", back_populates="game")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    release_date = Column(String, nullable=True)
    director = Column(String, nullable=True)
    writers = Column(JSON, default=list)
    producers = Column(JSON, default=list)
    cinematographer = Column(String, nullable=True)
    music_composer = Column(String, nullable=True)
    studio = Column(String, nullable=True)
    awards = Column(JSON, default=list)
    trivia = Column(JSON, default=list)
    bts_facts = Column(JSON, default=list)
    cover_image = Column(String, nullable=True)
    similar_movies = Column(JSON, default=list)  # List of movie IDs or titles

    # Relationships
    user_associations = relationship("UserMovie", back_populates="movie")


class UserGame(Base):
    __tablename__ = "user_games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    status = Column(String, default="wishlist")  # wishlist, playing, completed
    rating = Column(Float, nullable=True)  # 1 to 10 scale or 1 to 5
    review = Column(Text, nullable=True)
    hours_played = Column(Float, default=0.0)
    completion_percentage = Column(Integer, default=0)
    favorite_mechanics = Column(JSON, default=list)
    favorite_characters = Column(JSON, default=list)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="games")
    game = relationship("Game", back_populates="user_associations")


class UserMovie(Base):
    __tablename__ = "user_movies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    status = Column(String, default="watchlist")  # watchlist, watched
    rating = Column(Float, nullable=True)  # 1 to 10 scale
    review = Column(Text, nullable=True)
    watched_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="movies")
    movie = relationship("Movie", back_populates="user_associations")


class Creator(Base):
    __tablename__ = "game_creators"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    platform = Column(String, nullable=False)  # youtube, twitch
    creator_name = Column(String, nullable=False)
    channel_url = Column(String, nullable=False)
    category = Column(String, nullable=False)  # lore, speedrun, esports, review, challenge

    # Relationships
    game = relationship("Game", back_populates="creators")


class AIMemory(Base):
    __tablename__ = "ai_memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    # Store dynamic preference profile as JSON
    # {
    #   "favorite_genres": {"RPG": 5, "Roguelike": 10},
    #   "favorite_directors": {"Christopher Nolan": 3},
    #   "favorite_actors": {"Cillian Murphy": 2},
    #   "favorite_studios": {"A24": 4},
    #   "favorite_developers": {"Supergiant Games": 5},
    #   "favorite_mechanics": {"Deckbuilding": 3},
    #   "favorite_visual_styles": {"Neon-Noir": 2},
    #   "movie_pacing": "Atmospheric/Slow",
    #   "game_difficulty": "Challenging"
    # }
    profile_json = Column(JSON, default=dict)
    long_term_notes = Column(Text, default="")
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="ai_memory")


class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_start = Column(DateTime, default=datetime.datetime.utcnow)
    insight_text = Column(Text, nullable=False)

    # Relationships
    user = relationship("User", back_populates="insights")
