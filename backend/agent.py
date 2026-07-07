import os
import json
import datetime
from sqlalchemy.orm import Session
from models import User, Game, Movie, UserGame, UserMovie, AIMemory, AIInsight, Creator

# Helper to run standard template fallback responses for Tyler
def generate_local_game_recommendations(user_profile, user_logged_game_ids, session: Session):
    # Fetch all games from DB
    all_games = session.query(Game).all()
    recommendations = []

    fav_genres = user_profile.get("favorite_genres", {})
    fav_devs = user_profile.get("favorite_developers", {})
    fav_mechanics = user_profile.get("favorite_mechanics", {})

    # Sort genres, devs, mechanics by weight
    sorted_genres = sorted(fav_genres.items(), key=lambda x: x[1], reverse=True)
    sorted_devs = sorted(fav_devs.items(), key=lambda x: x[1], reverse=True)
    sorted_mechanics = sorted(fav_mechanics.items(), key=lambda x: x[1], reverse=True)

    top_genre = sorted_genres[0][0] if sorted_genres else "Action"
    top_dev = sorted_devs[0][0] if sorted_devs else "FromSoftware"
    top_mechanic = sorted_mechanics[0][0] if sorted_mechanics else "Dodge roll"

    for game in all_games:
        if game.id in user_logged_game_ids:
            continue  # Skip games the user already logged

        # Simple semantic scoring
        score = 0
        reasons = []

        # Genre overlap
        genre_overlap = [g for g in (game.genre or []) if g in fav_genres]
        score += len(genre_overlap) * 2
        if top_genre in (game.genre or []):
            score += 3
            reasons.append(f"it fits your love for {top_genre} games")

        # Developer match
        if game.developer in fav_devs:
            score += 4
            reasons.append(f"it is crafted by {game.developer}, a developer you appreciate")
        elif game.developer == top_dev:
            score += 5
            reasons.append(f"it aligns with your history playing {top_dev} titles")

        # Mechanics overlap (we can mock mechanics for seeded games in descriptions/facts)
        # For simplicity, check if the game has similar mechanics in description
        game_desc_lower = (game.description or "").lower()
        matched_mechanics = []
        for mech in fav_mechanics:
            if mech.lower() in game_desc_lower:
                score += 3
                matched_mechanics.append(mech)
        
        if matched_mechanics:
            reasons.append(f"features the {', '.join(matched_mechanics)} mechanics you enjoy")

        # Fallback if no matching reasons
        if not reasons:
            reasons.append(f"its rich {game.genre[0] if game.genre else 'gameplay'} looks like a great fit for your collection")
            score += 1

        recommendations.append({
            "game_id": game.id,
            "title": game.title,
            "cover_image": game.cover_image,
            "developer": game.developer,
            "score": score,
            "reasons": reasons
        })

    # Sort by score desc
    recommendations.sort(key=lambda x: x["score"], reverse=True)

    # Convert to natural sentences
    final_recommends = []
    for rec in recommendations[:3]:
        # Formulate conversational reasoning sentence
        reason_sentence = ""
        if len(rec["reasons"]) >= 2:
            reason_sentence = f"Since you've spent a lot of time exploring {top_genre} games, I recommend **{rec['title']}** because {rec['reasons'][0]} and {rec['reasons'][1]}."
        else:
            reason_sentence = f"I recommend **{rec['title']}** as {rec['reasons'][0]}. It offers a beautifully realized world."
            
        final_recommends.append({
            "id": rec["game_id"],
            "title": rec["title"],
            "cover_image": rec["cover_image"],
            "developer": rec["developer"],
            "reason": reason_sentence
        })

    return final_recommends


def generate_local_movie_recommendations(user_profile, user_logged_movie_ids, session: Session):
    all_movies = session.query(Movie).all()
    recommendations = []

    fav_directors = user_profile.get("favorite_directors", {})
    fav_cinematographers = user_profile.get("favorite_cinematographers", {})
    fav_composers = user_profile.get("favorite_composers", {})

    sorted_directors = sorted(fav_directors.items(), key=lambda x: x[1], reverse=True)
    sorted_cinematographers = sorted(fav_cinematographers.items(), key=lambda x: x[1], reverse=True)
    sorted_composers = sorted(fav_composers.items(), key=lambda x: x[1], reverse=True)

    top_director = sorted_directors[0][0] if sorted_directors else "Denis Villeneuve"
    top_cinematographer = sorted_cinematographers[0][0] if sorted_cinematographers else "Roger Deakins"
    top_composer = sorted_composers[0][0] if sorted_composers else "Hans Zimmer"

    for movie in all_movies:
        if movie.id in user_logged_movie_ids:
            continue

        score = 0
        reasons = []

        if movie.director in fav_directors:
            score += 5
            reasons.append(f"directed by {movie.director}")
        elif movie.director == top_director:
            score += 6
            reasons.append(f"crafted by {top_director}, who directed several of your favorites")

        if movie.cinematographer in fav_cinematographers:
            score += 4
            reasons.append(f"features the gorgeous cinematography of {movie.cinematographer}")
        elif movie.cinematographer == top_cinematographer:
            score += 5
            reasons.append(f"shot by {top_cinematographer}, matching your eye for visual style")

        if movie.music_composer in fav_composers:
            score += 3
            reasons.append(f"scored by composer {movie.music_composer}")
        elif movie.music_composer == top_composer:
            score += 4
            reasons.append(f"features the sweeping orchestral score of {top_composer}")

        if not reasons:
            reasons.append("fits your appreciation for atmospheric and cinematic visual storytelling")
            score += 1

        recommendations.append({
            "movie_id": movie.id,
            "title": movie.title,
            "cover_image": movie.cover_image,
            "director": movie.director,
            "score": score,
            "reasons": reasons
        })

    recommendations.sort(key=lambda x: x["score"], reverse=True)

    final_recommends = []
    for rec in recommendations[:3]:
        reason_sentence = ""
        if len(rec["reasons"]) >= 2:
            reason_sentence = f"I've noticed you rate {top_director} films highly. You should watch **{rec['title']}**, as it is {rec['reasons'][0]} and {rec['reasons'][1]}."
        else:
            reason_sentence = f"You might appreciate **{rec['title']}** because it {rec['reasons'][0]}. It has an incredible cinematic feel."
            
        final_recommends.append({
            "id": rec["movie_id"],
            "title": rec["title"],
            "cover_image": rec["cover_image"],
            "director": rec["director"],
            "reason": reason_sentence
        })

    return final_recommends


class TylerAgent:
    def __init__(self):
        # We can fetch API keys from the environment if present
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def update_user_profile(self, user_id: int, session: Session):
        # 1. Fetch user games & movies
        user_games = session.query(UserGame).filter_by(user_id=user_id).all()
        user_movies = session.query(UserMovie).filter_by(user_id=user_id).all()

        # Compile preferences
        favorite_genres = {}
        favorite_developers = {}
        favorite_mechanics = {}
        favorite_directors = {}
        favorite_cinematographers = {}
        favorite_composers = {}
        favorite_studios = {}

        total_game_hours = 0.0
        completed_games_count = 0
        total_game_ratings = 0
        game_rating_sum = 0.0

        for ug in user_games:
            game = session.query(Game).filter_by(id=ug.game_id).first()
            if not game:
                continue

            total_game_hours += ug.hours_played
            if ug.status == "completed":
                completed_games_count += 1
            if ug.rating:
                total_game_ratings += 1
                game_rating_sum += ug.rating

            # Genre weights
            weight = ug.rating if ug.rating else 5.0
            for g in (game.genre or []):
                favorite_genres[g] = favorite_genres.get(g, 0.0) + weight

            # Developer weights
            if game.developer:
                favorite_developers[game.developer] = favorite_developers.get(game.developer, 0.0) + weight

            # Mechanics weights
            for mech in (ug.favorite_mechanics or []):
                favorite_mechanics[mech] = favorite_mechanics.get(mech, 0.0) + 1.0

        total_movie_ratings = 0
        movie_rating_sum = 0.0

        for um in user_movies:
            movie = session.query(Movie).filter_by(id=um.movie_id).first()
            if not movie:
                continue

            weight = um.rating if um.rating else 5.0
            if um.rating:
                total_movie_ratings += 1
                movie_rating_sum += um.rating

            if movie.director:
                favorite_directors[movie.director] = favorite_directors.get(movie.director, 0.0) + weight
            if movie.cinematographer:
                favorite_cinematographers[movie.cinematographer] = favorite_cinematographers.get(movie.cinematographer, 0.0) + weight
            if movie.music_composer:
                favorite_composers[movie.music_composer] = favorite_composers.get(movie.music_composer, 0.0) + weight
            if movie.studio:
                favorite_studios[movie.studio] = favorite_studios.get(movie.studio, 0.0) + weight

        # Compile final profile
        profile = {
            "favorite_genres": favorite_genres,
            "favorite_developers": favorite_developers,
            "favorite_mechanics": favorite_mechanics,
            "favorite_directors": favorite_directors,
            "favorite_cinematographers": favorite_cinematographers,
            "favorite_composers": favorite_composers,
            "favorite_studios": favorite_studios,
            "total_game_hours": total_game_hours,
            "completed_games_count": completed_games_count,
            "avg_game_rating": round(game_rating_sum / total_game_ratings, 1) if total_game_ratings else 0,
            "avg_movie_rating": round(movie_rating_sum / total_movie_ratings, 1) if total_movie_ratings else 0,
            "movie_pacing": "Atmospheric/Slow" if len(favorite_cinematographers) > 0 else "Balanced",
            "game_difficulty": "Challenging" if "Soulslike" in favorite_genres or "FromSoftware" in favorite_developers else "Balanced"
        }

        # Check and get existing AI memory
        ai_mem = session.query(AIMemory).filter_by(user_id=user_id).first()
        if not ai_mem:
            ai_mem = AIMemory(user_id=user_id)
            session.add(ai_mem)
        
        ai_mem.profile_json = profile
        session.commit()
        return profile

    def get_recommendations(self, user_id: int, item_type: str, session: Session):
        # Ensure memory exists
        ai_mem = session.query(AIMemory).filter_by(user_id=user_id).first()
        if not ai_mem or not ai_mem.profile_json:
            self.update_user_profile(user_id, session)
            ai_mem = session.query(AIMemory).filter_by(user_id=user_id).first()

        profile = ai_mem.profile_json

        if item_type == "game":
            user_logged_game_ids = [ug.game_id for ug in session.query(UserGame).filter_by(user_id=user_id).all()]
            # If LLM API keys exist, we could call them. Otherwise, run the beautiful semantic matching fallback.
            return generate_local_game_recommendations(profile, user_logged_game_ids, session)
        else:
            user_logged_movie_ids = [um.movie_id for um in session.query(UserMovie).filter_by(user_id=user_id).all()]
            return generate_local_movie_recommendations(profile, user_logged_movie_ids, session)

    def generate_weekly_insights(self, user_id: int, session: Session):
        # Query logs from past 7 days (or all logs if mock is needed)
        user_games = session.query(UserGame).filter_by(user_id=user_id).all()
        user_movies = session.query(UserMovie).filter_by(user_id=user_id).all()

        ai_mem = session.query(AIMemory).filter_by(user_id=user_id).first()
        profile = ai_mem.profile_json if ai_mem else {}

        # Synthesize local insights
        insights = []

        total_hours = profile.get("total_game_hours", 0.0)
        completed_games = profile.get("completed_games_count", 0)

        # Gamified level calculations
        total_logs = len(user_games) + len(user_movies)

        # Ranks: Observer, Explorer, Collector, Completionist, Curator, Archivist, Legend
        rank = "Observer"
        if total_logs >= 30:
            rank = "Legend"
        elif total_logs >= 20:
            rank = "Archivist"
        elif total_logs >= 12:
            rank = "Curator"
        elif total_logs >= 7:
            rank = "Completionist"
        elif total_logs >= 4:
            rank = "Collector"
        elif total_logs >= 1:
            rank = "Explorer"

        # Update User XP and Rank
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.rank = rank
            user.xp = total_logs * 100 + int(total_hours * 10)
            session.commit()

        # Build natural insights
        if total_hours > 0:
            insights.append(f"This week you explored {int(total_hours)} hours of interactive worlds. Your dedication to uncovering hidden mechanics is growing.")
        
        # Analyze movies watched
        composers = profile.get("favorite_composers", {})
        if composers:
            top_composer = max(composers, key=composers.get)
            insights.append(f"You have watched several films featuring composer {top_composer}. Your appreciation for sweeping, atmospheric scores is becoming a defining feature of your cinematic taste.")
        
        directors = profile.get("favorite_directors", {})
        if directors:
            top_director = max(directors, key=directors.get)
            insights.append(f"Christopher Nolan appears in {int(directors.get(top_director, 0)/5)} of your highest-rated film logged entries. You seem drawn to grand, conceptually challenging storytelling.")

        # Default insights if empty log
        if not insights:
            insights.append("Welcome to leesure! Start logging games and movies you've experienced. I will observe your choices and slowly compile your aesthetic profile.")
            insights.append("Your journey begins. As you log ratings and favorite directors or developers, I'll generate custom recommendations.")

        combined_insight_text = "\n\n".join(insights)

        # Save to DB
        insight_entry = AIInsight(user_id=user_id, insight_text=combined_insight_text)
        session.add(insight_entry)
        session.commit()

        return combined_insight_text
