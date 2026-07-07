import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add current folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Base, Game, Movie, Creator, User

DATABASE_URL = "sqlite:///./leesure.db"

def seed_database():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

    # --- POPULATE GAMES ---
    games_data = [
        # ── Detailed catalog entries (rich metadata) ──
        {
            "id": 1,
            "title": "Elden Ring",
            "release_date": "2022-02-25",
            "developer": "FromSoftware",
            "publisher": "Bandai Namco",
            "genre": ["RPG", "Soulslike", "Action", "Open World"],
            "platforms": ["PC", "PS5", "Xbox Series X"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_art.jpg",
            "description": "Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring and become an Elden Lord in the Lands Between. Explore a vast open world filled with challenging boss battles and deep environmental lore.",
            "screenshots": [
                "https://images.unsplash.com/photo-1612287230202-1bf1d85d1bdf?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80"
            ],
            "trailers": ["https://www.youtube.com/embed/E3Huy2cdih0"],
            "interesting_facts": [
                "The world's lore was co-created by fantasy novelist George R.R. Martin.",
                "Elden Ring won Game of the Year at The Game Awards 2022."
            ],
            "news": [
                "Shadow of the Erdtree DLC sells over 5 million copies in its first week.",
                "New patch balances colosseum PvP combat scaling."
            ],
            "community_discussions": [
                "Is Malenia the hardest boss in FromSoftware history?",
                "Deciphering the connection between the Greater Will and the Frenzied Flame."
            ],
            "dlc_info": [
                {"title": "Shadow of the Erdtree", "type": "Expansion", "release": "2024-06-21"}
            ],
            "similar_games": ["Lies of P", "Sekiro: Shadows Die Twice", "Hollow Knight"]
        },
        {
            "id": 2,
            "title": "Hades",
            "release_date": "2020-09-17",
            "developer": "Supergiant Games",
            "publisher": "Supergiant Games",
            "genre": ["Roguelike", "Action", "Indie", "Isometric"],
            "platforms": ["PC", "Nintendo Switch", "PS5", "Xbox Series X"],
            "cover_image": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&w=600&q=80",
            "description": "Defy the god of the dead as you hack and slash out of the Underworld in this rogue-like dungeon crawler from the creators of Bastion, Transistor, and Pyre.",
            "screenshots": [
                "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80"
            ],
            "trailers": ["https://www.youtube.com/embed/91t0ha9x0Y8"],
            "interesting_facts": [
                "Hades was the first video game to ever win a Hugo Award.",
                "The game features over 300,000 words of spoken dialogue, dynamically reacting to user choices."
            ],
            "news": [
                "Supergiant Games announces work on post-launch patches for Hades II.",
                "Hades vinyl soundtrack back in stock at Supergiant store."
            ],
            "community_discussions": [
                "Which weapon aspect is your go-to for Heat 20+ runs?",
                "The emotional weight of reuniting Orpheus and Eurydice."
            ],
            "dlc_info": [],
            "similar_games": ["Dead Cells", "Slay the Spire", "Astral Ascent"]
        },
        {
            "id": 3,
            "title": "Dead Cells",
            "release_date": "2018-08-07",
            "developer": "Motion Twin",
            "publisher": "Motion Twin",
            "genre": ["Roguelike", "Metroidvania", "Action", "Indie"],
            "platforms": ["PC", "Nintendo Switch", "PS4", "Xbox One"],
            "cover_image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80",
            "description": "Dead Cells is a rogue-lite, metroidvania action-platformer. You'll explore a sprawling, ever-changing castle... assuming you're able to fight your way past its keepers in 2D souls-lite combat.",
            "screenshots": [],
            "trailers": ["https://www.youtube.com/embed/RvGaSp128SU"],
            "interesting_facts": [
                "The developers utilize a cooperative structure where all members receive equal pay.",
                "The game features collaboration crossovers with Hollow Knight, Castlevania, Hotline Miami, and more."
            ],
            "news": [
                "The 'Return to Castlevania' expansion wins indie DLC accolades.",
                "Final content update 'The End is Near' now live."
            ],
            "community_discussions": [
                "How do you beat the Hand of the King on 5 Boss Cells?",
                "Best build combinations using the Panchaku."
            ],
            "dlc_info": [
                {"title": "Return to Castlevania", "type": "DLC", "release": "2023-03-06"},
                {"title": "The Queen and the Sea", "type": "DLC", "release": "2022-01-06"}
            ],
            "similar_games": ["Hades", "Hollow Knight", "Ravenswatch"]
        },
        {
            "id": 4,
            "title": "Lies of P",
            "release_date": "2023-09-18",
            "developer": "Round8 Studio",
            "publisher": "NEOWIZ",
            "genre": ["RPG", "Soulslike", "Action", "Dark Fantasy"],
            "platforms": ["PC", "PS5", "Xbox Series X"],
            "cover_image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=600&q=80",
            "description": "You are a puppet created by Geppetto who's caught in a web of lies with unimaginable monsters and untrustworthy figures standing between you and the events that have befallen the city of Krat.",
            "screenshots": [],
            "trailers": ["https://www.youtube.com/embed/s3M5o9pS6Yw"],
            "interesting_facts": [
                "The game is a dark adaptation of Carlo Collodi's Pinocchio story.",
                "Lies of P won several awards for its elegant weapon assembly mechanics."
            ],
            "news": [
                "Developer releases roadmap showing upcoming DLC and sequel concept art.",
                "Patch 1.3 smooths out early-game boss difficulty curves."
            ],
            "community_discussions": [
                "The perfectionism of the Guard Regain mechanic.",
                "Lying vs Telling the Truth: Which ending did you get?"
            ],
            "dlc_info": [],
            "similar_games": ["Elden Ring", "Sekiro: Shadows Die Twice", "Nine Sols"]
        },
        {
            "id": 5,
            "title": "Nine Sols",
            "release_date": "2024-05-29",
            "developer": "Red Candle Games",
            "publisher": "Red Candle Games",
            "genre": ["Action", "Metroidvania", "Soulslike", "Indie"],
            "platforms": ["PC", "Nintendo Switch", "PS5", "Xbox Series X"],
            "cover_image": "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?auto=format&fit=crop&w=600&q=80",
            "description": "Nine Sols is a lore-rich, hand-drawn 2D action-platformer featuring Sekiro-inspired deflection-focused combat. Embark on a journey in an Asian fantasy setting to slay the 9 Sols, formidable rulers of a forsaken realm.",
            "screenshots": [],
            "trailers": ["https://www.youtube.com/embed/A9cKk9v8d1s"],
            "interesting_facts": [
                "Red Candle Games previously developed the atmospheric horror games Detention and Devotion.",
                "The developers coin their art style 'Taopunk', blending Taoist mythology with cyberpunk elements."
            ],
            "news": [
                "Nine Sols releases its critically acclaimed soundtrack on Spotify.",
                "Console release dates confirmed for Q4 2024."
            ],
            "community_discussions": [
                "Is Jiequan the most satisfying deflection fight in 2D gaming?",
                "The tragic lore of the Apocrypha and Solarian civilization."
            ],
            "dlc_info": [],
            "similar_games": ["Sekiro: Shadows Die Twice", "Lies of P", "Hollow Knight"]
        },
        {
            "id": 6,
            "title": "Slay the Spire",
            "release_date": "2019-01-23",
            "developer": "Mega Crit Games",
            "publisher": "Mega Crit Games",
            "genre": ["Roguelike", "Deckbuilding", "Strategy", "Indie"],
            "platforms": ["PC", "Nintendo Switch", "iOS", "Android", "PS4"],
            "cover_image": "https://images.unsplash.com/photo-1611195974226-a6a9be9dd763?auto=format&fit=crop&w=600&q=80",
            "description": "We fused card games and roguelikes together to make the best single player deckbuilder we could. Craft a unique deck, encounter bizarre creatures, discover relics of immense power, and Slay the Spire!",
            "screenshots": [],
            "trailers": ["https://www.youtube.com/embed/9Lsp2NtzKy4"],
            "interesting_facts": [
                "The game revitalized the entire roguelike deckbuilding subgenre.",
                "Slay the Spire II has been officially announced, built in the open-source Godot engine."
            ],
            "news": [
                "Mega Crit clarifies transition to Godot engine for Slay the Spire II.",
                "Board game adaptation raises millions on Kickstarter."
            ],
            "community_discussions": [
                "How to consistently beat Ascension 20 with the Defect.",
                "Which relics are immediate skips in Act 1?"
            ],
            "dlc_info": [],
            "similar_games": ["Hades", "Astral Ascent", "Children of Morta"]
        },
        {
            "id": 7,
            "title": "Sekiro: Shadows Die Twice",
            "release_date": "2019-03-22",
            "developer": "FromSoftware",
            "publisher": "Activision",
            "genre": ["Action", "Soulslike", "Stealth", "Adventure"],
            "platforms": ["PC", "PS4", "Xbox One"],
            "cover_image": "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?auto=format&fit=crop&w=600&q=80",
            "description": "Carve your own clever path to vengeance in the award-winning adventure from developer FromSoftware, creators of Bloodborne and the Dark Souls series. In Sekiro, you are the 'one-armed wolf', a disgraced warrior rescued from the brink of death.",
            "screenshots": [],
            "trailers": ["https://www.youtube.com/embed/rXMX4YJ7LGP"],
            "interesting_facts": [
                "Unlike other FromSoftware games, Sekiro does not have character customization or leveling stats, forcing players to master deflection.",
                "It won Game of the Year at The Game Awards 2019."
            ],
            "news": [
                "Sekiro passes 10 million units sold worldwide.",
                "Speedrunners break 19 minutes in the Any% glitchless category."
            ],
            "community_discussions": [
                "How to master the rhythm of the Sword Saint Isshin boss fight.",
                "Why the posture system is superior to traditional stamina bars."
            ],
            "dlc_info": [],
            "similar_games": ["Nine Sols", "Lies of P", "Elden Ring"]
        },
        {
            "id": 8,
            "title": "Astral Ascent",
            "release_date": "2023-11-14",
            "developer": "Hibernian Workshop",
            "publisher": "Hibernian Workshop",
            "genre": ["Roguelike", "Action", "Platformer", "Indie"],
            "platforms": ["PC", "Nintendo Switch", "PS5"],
            "cover_image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=600&q=80",
            "description": "Astral Ascent is a 2D platformer rogue-lite game set in a modern fantasy world. As one of the 4 characters, you must escape the Garden, an astral prison guarded by 12 powerful Zodiac bosses.",
            "screenshots": [],
            "trailers": ["https://www.youtube.com/embed/U3lW82R_7pU"],
            "interesting_facts": [
                "Features fully voiced characters and a cinematic animated opening sequence.",
                "Incorporates an intricate spell synergy system where players combine standard spells with elements like Poison and Spark."
            ],
            "news": [
                "Update 1.6 introduces local co-op gameplay tweaks.",
                "Developer releases a sneak peek of the upcoming DLC containing a fifth character."
            ],
            "similar_games": ["Hades", "Dead Cells", "Ravenswatch"]
        },
        {
            "id": 9,
            "title": "Ravenswatch",
            "release_date": "2024-09-26",
            "developer": "Passtech Games",
            "publisher": "Nacon",
            "genre": ["Roguelike", "Action", "Isometric", "Co-op"],
            "platforms": ["PC", "PS5", "Xbox Series X"],
            "cover_image": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=600&q=80",
            "description": "Ravenswatch is a top-down action rogue-like that combines intense real-time combat with deep gameplay and high replay value. From the creators of Curse of the Dead Gods, play solo or with up to four players in co-op.",
            "screenshots": [],
            "trailers": ["https://www.youtube.com/embed/5F2v_25gHSw"],
            "interesting_facts": [
                "Characters are dark, combat-oriented adaptations of classic fairy tales (e.g. Scarlet/Little Red Riding Hood is a werewolf at night).",
                "Includes a strict 18-minute day/night cycle before the final boss portal opens."
            ],
            "news": [
                "1.0 version leaves Early Access with the addition of the third act and final boss.",
                "Passtech outlines roadmap for console ports."
            ],
            "similar_games": ["Hades", "Dead Cells", "Children of Morta"]
        },
        {
            "id": 10,
            "title": "Children of Morta",
            "release_date": "2019-09-03",
            "developer": "Dead Mage",
            "publisher": "11 bit studios",
            "genre": ["Roguelike", "RPG", "Indie", "Co-op"],
            "platforms": ["PC", "Nintendo Switch", "PS4", "Xbox One"],
            "cover_image": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=600&q=80",
            "description": "Children of Morta is an action RPG with a rogue-lite approach to character development, where you don't play a single character - but a whole, extraordinary family of heroes. Hack and slash through hordes of enemies in procedurally generated dungeons.",
            "screenshots": [],
            "trailers": ["https://www.youtube.com/embed/rG_M5NqJ1rQ"],
            "interesting_facts": [
                "The narration details the family's daily lives and conflicts in their mountaintop house between runs.",
                "Charity DLC 'Paws and Claws' raised thousands of dollars for animal protection charities."
            ],
            "news": [
                "Online co-op feature successfully added to all platforms.",
                "11 bit studios announces milestone of 1 million copies sold."
            ],
            "similar_games": ["Hades", "Ravenswatch", "Slay the Spire"]
        },

        # ── IGN Top Games Catalog (with real posters) ──
        {
            "id": 11,
            "title": "The Legend of Zelda: Ocarina of Time",
            "release_date": "1998-11-21",
            "developer": "Nintendo EAD",
            "publisher": "Nintendo",
            "genre": ["Action-Adventure", "RPG"],
            "platforms": ["Nintendo 64", "GameCube", "3DS"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/5/5e/The_Legend_of_Zelda_Ocarina_of_Time_box_art.png",
            "description": "Widely regarded as one of the greatest video games ever made, Ocarina of Time follows Link through the land of Hyrule on a quest to stop the evil Ganondorf using the power of the mystical Triforce.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "One of the highest rated video games of all time on Metacritic.",
                "Pioneered the Z-targeting combat system still used in many modern games."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["The Legend of Zelda: Breath of the Wild", "Shadow of the Colossus"]
        },
        {
            "id": 12,
            "title": "Super Mario 64",
            "release_date": "1996-06-23",
            "developer": "Nintendo EAD",
            "publisher": "Nintendo",
            "genre": ["3D Platformer"],
            "platforms": ["Nintendo 64"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/6/6a/Super_Mario_64_box_cover.jpg",
            "description": "The game that defined 3D platforming. Mario must rescue Princess Peach from Bowser's castle by collecting Power Stars across 15 vast 3D worlds.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Introduced the concept of free-roaming 3D gameplay to mainstream audiences.",
                "The BLJ (Backwards Long Jump) became one of gaming's most iconic speedrunning glitches."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Super Mario World", "Super Mario Bros. 3"]
        },
        {
            "id": 13,
            "title": "The Legend of Zelda: Breath of the Wild",
            "release_date": "2017-03-03",
            "developer": "Nintendo EPD",
            "publisher": "Nintendo",
            "genre": ["Action-Adventure", "Open World", "RPG"],
            "platforms": ["Nintendo Switch", "Wii U"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/c/c6/The_Legend_of_Zelda_Breath_of_the_Wild.jpg",
            "description": "A landmark open-world game that redefined exploration. Link awakens with no memories and must reclaim Hyrule from the Calamity Ganon across a massive, dynamic open world.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Won Game of the Year at The Game Awards 2017.",
                "Features a fully physics-driven world — nearly every interaction follows real-world physics rules."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Elden Ring", "The Witcher 3: Wild Hunt"]
        },
        {
            "id": 14,
            "title": "Grand Theft Auto V",
            "release_date": "2013-09-17",
            "developer": "Rockstar North",
            "publisher": "Rockstar Games",
            "genre": ["Action-Adventure", "Open World", "Crime"],
            "platforms": ["PC", "PS4", "Xbox One", "PS5", "Xbox Series X"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/a/a5/Grand_Theft_Auto_V.png",
            "description": "Set in the sprawling city of Los Santos, GTA V follows three protagonists — Michael, Trevor, and Franklin — as they plan and execute daring heists across the open world.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "One of the best-selling video games of all time, with over 190 million copies sold.",
                "GTA Online has continued to generate revenue for over a decade post-release."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Red Dead Redemption 2"]
        },
        {
            "id": 15,
            "title": "Super Mario Bros. 3",
            "release_date": "1988-10-23",
            "developer": "Nintendo R&D4",
            "publisher": "Nintendo",
            "genre": ["2D Platformer"],
            "platforms": ["NES", "Game Boy Advance"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/a/a5/Super_Mario_Bros._3_coverart.png",
            "description": "Often considered the pinnacle of 2D Mario games. Mario travels through eight diverse worlds to rescue Princess Peach and save the Mushroom Kings from Bowser's children.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "The game was famously featured in the movie 'The Wizard' before its US release.",
                "Introduced iconic power-ups like the Tanooki Suit and the Frog Suit."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Super Mario World", "Super Mario 64"]
        },
        {
            "id": 16,
            "title": "Half-Life 2",
            "release_date": "2004-11-16",
            "developer": "Valve",
            "publisher": "Valve",
            "genre": ["FPS", "Sci-Fi", "Action"],
            "platforms": ["PC", "Xbox", "PS3"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/2/25/Half-Life_2_cover.jpg",
            "description": "Gordon Freeman returns in this landmark FPS, armed with the gravity gun and surrounded by compelling characters, as he leads a resistance against the alien Combine empire.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Introduced the Source Engine, which revolutionized facial animation and physics in games.",
                "Won over 39 Game of the Year awards upon release."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Portal 2", "BioShock"]
        },
        {
            "id": 17,
            "title": "Red Dead Redemption 2",
            "release_date": "2018-10-26",
            "developer": "Rockstar Games",
            "publisher": "Rockstar Games",
            "genre": ["Action-Adventure", "Open World", "Western"],
            "platforms": ["PS4", "Xbox One", "PC"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/4/44/Red_Dead_Redemption_II.jpg",
            "description": "A prequel to the original Red Dead Redemption. Arthur Morgan navigates the twilight of the outlaw era, balancing loyalty to his gang with his own morality in a stunning open world.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Features the most detailed open world ever created at launch, with over 200 species of animals.",
                "Took over 8 years and 1,600 developers to create."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Grand Theft Auto V", "The Witcher 3: Wild Hunt"]
        },
        {
            "id": 18,
            "title": "Minecraft",
            "release_date": "2011-11-18",
            "developer": "Mojang Studios",
            "publisher": "Mojang Studios / Microsoft",
            "genre": ["Sandbox", "Survival", "Creative"],
            "platforms": ["PC", "PS4", "Xbox One", "Nintendo Switch", "iOS", "Android"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/5/51/Minecraft_cover.png",
            "description": "The best-selling video game of all time. Players explore and build in procedurally generated worlds of blocks, surviving against monsters or creating virtually anything imaginable.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "The best-selling video game of all time with over 300 million copies sold.",
                "Originally created by a single developer, Markus 'Notch' Persson, in just six days."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Terraria", "Stardew Valley"]
        },
        {
            "id": 19,
            "title": "Portal 2",
            "release_date": "2011-04-19",
            "developer": "Valve",
            "publisher": "Valve",
            "genre": ["Puzzle", "FPS", "Sci-Fi"],
            "platforms": ["PC", "PS3", "Xbox 360"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/f/f9/Portal2cover.jpg",
            "description": "Chell returns to the Aperture Science facility for more mind-bending portal puzzles, alongside the witty AI GLaDOS and the bumbling robot Wheatley.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "The co-op mode was designed so each player could only see through their own portals, encouraging communication.",
                "Stephen Merchant was cast as Wheatley after his voice was heard playing video games."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Half-Life 2", "BioShock"]
        },
        {
            "id": 20,
            "title": "The Last of Us",
            "release_date": "2013-06-14",
            "developer": "Naughty Dog",
            "publisher": "Sony Interactive Entertainment",
            "genre": ["Action-Adventure", "Survival Horror", "Narrative"],
            "platforms": ["PS3", "PS4", "PC"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/4/46/Video_Game_Cover_-_The_Last_of_Us.jpg",
            "description": "Joel, a hardened survivor, escorts the immune teenager Ellie across a post-apocalyptic United States overrun by the Cordyceps fungus, forging an unforgettable bond.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Inspired by a BBC documentary about a parasitic fungus that takes over ants' brains.",
                "Won over 200 Game of the Year awards."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["God of War (2018)", "Red Dead Redemption 2"]
        },
        {
            "id": 21,
            "title": "BioShock",
            "release_date": "2007-08-21",
            "developer": "2K Boston / Irrational Games",
            "publisher": "2K Games",
            "genre": ["FPS", "Action-RPG", "Horror", "Sci-Fi"],
            "platforms": ["PC", "Xbox 360", "PS3"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/6/6d/BioShock_cover.jpg",
            "description": "Discover the underwater city of Rapture, a utopia turned dystopia where plasmids have unleashed chaos. Fight through the crumbling art-deco city and unravel its dark secrets.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "The game's narrative is heavily inspired by Ayn Rand's philosophy of objectivism.",
                "Would You Kindly? remains one of gaming's most iconic narrative twists."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Half-Life 2", "System Shock 2"]
        },
        {
            "id": 22,
            "title": "Bloodborne",
            "release_date": "2015-03-24",
            "developer": "FromSoftware",
            "publisher": "Sony Interactive Entertainment",
            "genre": ["Action RPG", "Soulslike", "Gothic Horror"],
            "platforms": ["PS4"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/6/68/Bloodborne_Cover_Wallpaper.jpg",
            "description": "Explore the nightmarish gothic city of Yharnam, plagued by a beastly scourge, and unravel the dark secrets of the blood that both empowers and corrupts.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Lovecraftian cosmic horror permeates the game's late-game narrative.",
                "The Chalice Dungeons generate unique procedurally-generated underground areas."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Elden Ring", "Sekiro: Shadows Die Twice"]
        },
        {
            "id": 23,
            "title": "The Witcher 3: Wild Hunt",
            "release_date": "2015-05-19",
            "developer": "CD Projekt Red",
            "publisher": "CD Projekt",
            "genre": ["RPG", "Open World", "Fantasy"],
            "platforms": ["PC", "PS4", "Xbox One", "Nintendo Switch", "PS5", "Xbox Series X"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/0/0c/Witcher_3_cover_art.jpg",
            "description": "Geralt of Rivia, a monster hunter for hire, searches the vast open world for his adopted daughter Ciri while navigating politics and war across a richly realized fantasy world.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Won over 250 Game of the Year awards, a record at the time.",
                "The game's quests are so well-written that several were later turned into short stories."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Elden Ring", "Red Dead Redemption 2"]
        },
        {
            "id": 24,
            "title": "God of War (2018)",
            "release_date": "2018-04-20",
            "developer": "Santa Monica Studio",
            "publisher": "Sony Interactive Entertainment",
            "genre": ["Action-Adventure", "Norse Mythology", "Narrative"],
            "platforms": ["PS4", "PS5", "PC"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/a/a7/God_of_War_4_cover.jpg",
            "description": "Kratos and his son Atreus journey through the Nine Realms of Norse mythology in a single-take cinematic adventure that redefines the franchise with emotional depth and brutal combat.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "The entire game is filmed in a single unbroken camera shot with no cuts.",
                "Won Game of the Year at The Game Awards 2018."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Elden Ring", "The Last of Us"]
        },
        {
            "id": 25,
            "title": "Hollow Knight",
            "release_date": "2017-02-24",
            "developer": "Team Cherry",
            "publisher": "Team Cherry",
            "genre": ["Metroidvania", "Action", "Indie"],
            "platforms": ["PC", "Nintendo Switch", "PS4", "Xbox One"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/0/04/Hollow_Knight_first_cover_art.webp",
            "description": "Delve into the ancient, ruined kingdom of Hallownest, fighting through its many kingdoms and bosses as a small, silent, nameless knight.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Made by a team of just three people over several years.",
                "Features over 40 boss fights and a sprawling interconnected world."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Dead Cells", "Nine Sols", "Elden Ring"]
        },
        {
            "id": 26,
            "title": "Persona 5 Royal",
            "release_date": "2020-03-31",
            "developer": "Atlus",
            "publisher": "Atlus",
            "genre": ["JRPG", "Life Simulation", "Turn-Based"],
            "platforms": ["PS4", "PS5", "PC", "Xbox Series X", "Nintendo Switch"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/b/b0/Persona_5_cover_art.jpg",
            "description": "High school student Ren Amamiya and his Phantom Thieves change the hearts of corrupt adults through the mysterious Metaverse, all while navigating everyday school life in Tokyo.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Features over 100+ hours of content in the Royal expanded edition.",
                "The game's iconic red-and-black art style was inspired by heist films."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Chrono Trigger", "Final Fantasy VII"]
        },
        {
            "id": 27,
            "title": "Mass Effect 2",
            "release_date": "2010-01-26",
            "developer": "BioWare",
            "publisher": "EA",
            "genre": ["Action RPG", "Sci-Fi", "Third-Person Shooter"],
            "platforms": ["PC", "Xbox 360", "PS3"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/0/05/MassEffect2_cover.PNG",
            "description": "Commander Shepard is resurrected to lead a suicide mission against the Collectors. Recruit a team of loyal specialists and forge bonds that determine who survives.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Often called the Empire Strikes Back of video games.",
                "Every party member has a unique loyalty mission that can end in their death."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["BioShock", "The Witcher 3: Wild Hunt"]
        },
        {
            "id": 28,
            "title": "Shadow of the Colossus",
            "release_date": "2005-10-18",
            "developer": "Team Ico",
            "publisher": "Sony Interactive Entertainment",
            "genre": ["Action-Adventure", "Art Game"],
            "platforms": ["PS2", "PS3", "PS4"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/9/90/Shadow_of_the_Colossus_cover_art.png",
            "description": "Wander must slay sixteen massive colossi across a desolate landscape to resurrect a mysterious girl. A haunting, minimalist masterpiece with no other enemies.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "The game features 16 colossi and nothing else — no other enemies exist.",
                "Its emotional ending is considered one of gaming's most powerful moments."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Hollow Knight", "The Last of Us"]
        },
        {
            "id": 29,
            "title": "Chrono Trigger",
            "release_date": "1995-03-11",
            "developer": "Square",
            "publisher": "Square",
            "genre": ["JRPG", "Turn-Based", "Time Travel"],
            "platforms": ["SNES", "DS", "PC"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/a/a7/Chrono_Trigger.jpg",
            "description": "Crono and his friends travel through time to prevent the apocalypse in this timeless JRPG, known for its revolutionary dual and triple tech combat system.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Created by the 'Dream Team' of Hironobu Sakaguchi, Yuji Horii, and Akira Toriyama.",
                "Features 13 different endings based on player choices."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Final Fantasy VII", "Persona 5 Royal"]
        },
        {
            "id": 30,
            "title": "Final Fantasy VII",
            "release_date": "1997-01-31",
            "developer": "Square",
            "publisher": "Square / Sony",
            "genre": ["JRPG", "Turn-Based", "Sci-Fantasy"],
            "platforms": ["PS1", "PC", "PS4", "Xbox One", "Nintendo Switch"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/c/c2/Final_Fantasy_VII_Box_Art.jpg",
            "description": "Cloud Strife joins the eco-terrorist group AVALANCHE to fight the Shinra Corporation, uncovering a deeper threat from the legendary Sephiroth along the way.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Aerith's death is considered one of the most emotional moments in gaming history.",
                "Moved the Final Fantasy series from 2D to 3D graphics and full-motion video cutscenes."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Chrono Trigger", "Persona 5 Royal"]
        },
        {
            "id": 31,
            "title": "Halo: Combat Evolved",
            "release_date": "2001-11-15",
            "developer": "Bungie",
            "publisher": "Microsoft",
            "genre": ["FPS", "Sci-Fi", "Action"],
            "platforms": ["Xbox", "PC"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/8/80/Halo_-_Combat_Evolved_Coverart.png",
            "description": "Master Chief and Cortana crash-land on the mysterious ring-world Halo and must stop the alien Covenant and their plan to unleash the terrifying Flood parasite.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "The game's AI was so advanced that enemies would flank, retreat, and coordinate attacks dynamically.",
                "Became the flagship launch title for the original Xbox, driving massive console sales."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Half-Life 2", "BioShock"]
        },
        {
            "id": 32,
            "title": "Super Metroid",
            "release_date": "1994-03-19",
            "developer": "Nintendo R&D1",
            "publisher": "Nintendo",
            "genre": ["Metroidvania", "Action-Adventure", "Sci-Fi"],
            "platforms": ["SNES"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/e/e4/Smetroidbox.jpg",
            "description": "Samus Aran returns to the planet Zebes to reclaim the last Metroid larva stolen by the Space Pirate leader Ridley. The genre-defining Metroidvania experience.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Coined the Metroidvania genre alongside Castlevania: Symphony of the Night.",
                "Its atmospheric storytelling is delivered entirely without dialogue."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Hollow Knight", "Dead Cells"]
        },
        {
            "id": 33,
            "title": "Tetris",
            "release_date": "1984-06-06",
            "developer": "Alexey Pajitnov",
            "publisher": "Nintendo",
            "genre": ["Puzzle"],
            "platforms": ["Game Boy", "NES", "PC", "iOS", "Android"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/8/8d/NES_Tetris_Box_Front.jpg",
            "description": "The world's most-played video game. Arrange falling Tetrimino blocks to clear lines and prevent the stack from reaching the top.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Created by Soviet software engineer Alexey Pajitnov in 1984.",
                "The Tetris effect is a real psychological phenomenon where players see falling blocks in their dreams."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Slay the Spire"]
        },
        {
            "id": 34,
            "title": "Super Mario World",
            "release_date": "1990-11-21",
            "developer": "Nintendo EAD",
            "publisher": "Nintendo",
            "genre": ["2D Platformer"],
            "platforms": ["SNES", "Game Boy Advance"],
            "cover_image": "https://upload.wikimedia.org/wikipedia/en/3/32/Super_Mario_World_Coverart.png",
            "description": "Mario and Luigi explore Dinosaur Land to rescue Princess Peach and Yoshi's friends in this SNES launch classic featuring 96 exits and the beloved Yoshi.",
            "screenshots": [],
            "trailers": [],
            "interesting_facts": [
                "Introduced Yoshi to the Mario franchise.",
                "Contains 72 levels with 96 exits, encouraging exploration."
            ],
            "news": [],
            "community_discussions": [],
            "dlc_info": [],
            "similar_games": ["Super Mario Bros. 3", "Super Mario 64"]
        },
    ]

    for g in games_data:
        game = Game(**g)
        session.add(game)

    # --- POPULATE GAME CREATORS ---
    creators_data = [
        # Elden Ring
        {"game_id": 1, "platform": "youtube", "creator_name": "VaatiVidya", "channel_url": "https://www.youtube.com/@VaatiVidya", "category": "lore"},
        {"game_id": 1, "platform": "youtube", "creator_name": "LilAggy", "channel_url": "https://www.youtube.com/@LilAggy", "category": "challenge"},
        {"game_id": 1, "platform": "twitch", "creator_name": "Distortion2", "channel_url": "https://www.twitch.tv/distortion2", "category": "speedrun"},
        # Hades
        {"game_id": 2, "platform": "youtube", "creator_name": "Haelian", "channel_url": "https://www.youtube.com/@Haelian", "category": "review"},
        {"game_id": 2, "platform": "youtube", "creator_name": "Jawless Paul", "channel_url": "https://www.youtube.com/@JawlessPaul", "category": "challenge"},
        # Sekiro
        {"game_id": 7, "platform": "youtube", "creator_name": "Ongbal", "channel_url": "https://www.youtube.com/@Ongbal", "category": "challenge"},
        # Nine Sols
        {"game_id": 5, "platform": "youtube", "creator_name": "Aliensrock", "channel_url": "https://www.youtube.com/@Aliensrock", "category": "review"}
    ]

    for c in creators_data:
        creator = Creator(**c)
        session.add(creator)

    # --- POPULATE MOVIES ---
    movies_data = [
        # ── Detailed catalog entries (rich metadata) ──
        {
            "id": 101,
            "title": "Interstellar",
            "release_date": "2014-11-07",
            "director": "Christopher Nolan",
            "writers": ["Jonathan Nolan", "Christopher Nolan"],
            "producers": ["Emma Thomas", "Christopher Nolan", "Lynda Obst"],
            "cinematographer": "Hoyte van Hoytema",
            "music_composer": "Hans Zimmer",
            "studio": "Paramount Pictures / Legendary",
            "awards": ["Academy Award for Best Visual Effects", "BAFTA Award for Best Special Visual Effects"],
            "trivia": [
                "Dr. Kip Thorne wrote two scientific papers based on the rendering engine developed for the black hole Gargantua.",
                "Hans Zimmer composed the score without knowing the film's genre; Nolan only gave him a one-page text about a father leaving his child."
            ],
            "bts_facts": [
                "Nolan grew 500 acres of real corn fields specifically to burn them for the dust storm scenes.",
                "The robotic characters TARS and CASE were physical puppets operated on set by actor Bill Irwin."
            ],
            "cover_image": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
            "similar_movies": ["Inception", "Arrival", "Oppenheimer"]
        },
        {
            "id": 102,
            "title": "Inception",
            "release_date": "2010-07-16",
            "director": "Christopher Nolan",
            "writers": ["Christopher Nolan"],
            "producers": ["Emma Thomas", "Christopher Nolan"],
            "cinematographer": "Wally Pfister",
            "music_composer": "Hans Zimmer",
            "studio": "Warner Bros. Pictures",
            "awards": ["Academy Award for Best Cinematography", "Academy Award for Best Visual Effects"],
            "trivia": [
                "The film's runtime (2 hours 28 minutes) is a reference to Edith Piaf's song 'Non, je ne regrette rien' which lasts 2 minutes 28 seconds.",
                "Leonardo DiCaprio was the only choice for the role of Cobb."
            ],
            "bts_facts": [
                "The rotating hallway fight scene was shot using a massive custom centrifuge construct that rotated 360 degrees.",
                "No green screen was used during the cafe explosion scene; air cannons blew real debris at high-speed cameras."
            ],
            "cover_image": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
            "similar_movies": ["Interstellar", "Blade Runner 2049", "Arrival"]
        },
        {
            "id": 103,
            "title": "Blade Runner 2049",
            "release_date": "2017-10-06",
            "director": "Denis Villeneuve",
            "writers": ["Hampton Fancher", "Michael Green"],
            "producers": ["Broderick Johnson", "Andrew A. Kosove"],
            "cinematographer": "Roger Deakins",
            "music_composer": "Hans Zimmer",
            "studio": "Alcon Entertainment / Columbia",
            "awards": ["Academy Award for Best Cinematography", "Academy Award for Best Visual Effects"],
            "trivia": [
                "Roger Deakins won his first Academy Award for Best Cinematography with this film, after 14 nominations.",
                "Harrison Ford accidentally punched Ryan Gosling in the face during a fight scene."
            ],
            "bts_facts": [
                "Most of the futuristic city shots utilized massive architectural miniatures rather than CGI backdrops.",
                "The colored mist in Las Vegas was inspired by sandstorms in Sydney, Australia."
            ],
            "cover_image": "https://images.unsplash.com/photo-1515621061946-eff1c2a352bd?auto=format&fit=crop&w=600&q=80",
            "similar_movies": ["Arrival", "Sicario", "Inception"]
        },
        {
            "id": 104,
            "title": "Dune",
            "release_date": "2021-10-22",
            "director": "Denis Villeneuve",
            "writers": ["Jon Spaihts", "Denis Villeneuve", "Eric Roth"],
            "producers": ["Mary Parent", "Denis Villeneuve", "Cale Boyter"],
            "cinematographer": "Greig Fraser",
            "music_composer": "Hans Zimmer",
            "studio": "Legendary Pictures / Warner Bros.",
            "awards": ["Academy Award for Best Original Score", "Academy Award for Best Cinematography"],
            "trivia": [
                "Hans Zimmer turned down Christopher Nolan's Tenet to work on Dune, as he was a lifelong fan of the book.",
                "To simulate the sound of walking on sand, sound designers stepped on dry, crusty snow."
            ],
            "bts_facts": [
                "A large portion of the desert scenes were shot in Jordan and Abu Dhabi, matching sunlight color grids.",
                "Timothée Chalamet wore a heavy rubber stillsuit in 110-degree heat."
            ],
            "cover_image": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=600&q=80",
            "similar_movies": ["Dune: Part Two", "Blade Runner 2049", "Interstellar"]
        },
        {
            "id": 105,
            "title": "Dune: Part Two",
            "release_date": "2024-03-01",
            "director": "Denis Villeneuve",
            "writers": ["Denis Villeneuve", "Jon Spaihts"],
            "producers": ["Mary Parent", "Cale Boyter", "Denis Villeneuve"],
            "cinematographer": "Greig Fraser",
            "music_composer": "Hans Zimmer",
            "studio": "Legendary Pictures / Warner Bros.",
            "awards": [],
            "trivia": [
                "Austin Butler trained for months in Kali knife fighting for his role as Feyd-Rautha.",
                "Denis Villeneuve insisted on shooting 100% of the film in IMAX format."
            ],
            "bts_facts": [
                "The black-and-white gladiator sequence on Giedi Prime was filmed using infrared cameras to make the skin look translucent.",
                "Sound designers recorded the wind rustling dry leaves in valleys to compile the sand worm mating calls."
            ],
            "cover_image": "https://images.unsplash.com/photo-1547483238-2cbf88bd1423?auto=format&fit=crop&w=600&q=80",
            "similar_movies": ["Dune", "Blade Runner 2049", "Arrival"]
        },
        {
            "id": 106,
            "title": "Oppenheimer",
            "release_date": "2023-07-21",
            "director": "Christopher Nolan",
            "writers": ["Christopher Nolan"],
            "producers": ["Emma Thomas", "Charles Roven", "Christopher Nolan"],
            "cinematographer": "Hoyte van Hoytema",
            "music_composer": "Ludwig Göransson",
            "studio": "Universal Pictures / Syncopy",
            "awards": ["Academy Award for Best Picture", "Academy Award for Best Director", "Academy Award for Best Cinematography"],
            "trivia": [
                "The film features zero CGI shots. All visual effects, including the Trinity test, were done practically.",
                "Cillian Murphy ate mostly an almond a day to achieve the gaunt look of Oppenheimer."
            ],
            "bts_facts": [
                "Kodak created the first-ever 65mm black-and-white film stock specifically to fit the IMAX cameras Nolan wanted to use.",
                "The town of Los Alamos was fully rebuilt on a mesa in New Mexico."
            ],
            "cover_image": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
            "similar_movies": ["Interstellar", "Inception", "Sicario"]
        },
        {
            "id": 107,
            "title": "Arrival",
            "release_date": "2016-11-11",
            "director": "Denis Villeneuve",
            "writers": ["Eric Heisserer"],
            "producers": ["Shawn Levy", "Dan Levine"],
            "cinematographer": "Bradford Young",
            "music_composer": "Jóhann Jóhannsson",
            "studio": "FilmNation Entertainment",
            "awards": ["Academy Award for Best Sound Editing"],
            "trivia": [
                "Based on the short story 'Story of Your Life' by Ted Chiang.",
                "A complete, functional alien logogram language was created for the movie, consisting of over 100 symbols."
            ],
            "bts_facts": [
                "The inside of the spacecraft was lined with dark soundproofing foam panels to absorb light and sound practically.",
                "Bradford Young used mostly natural lighting or low-light LED setups to capture the film's soft, gray tones."
            ],
            "cover_image": "https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?auto=format&fit=crop&w=600&q=80",
            "similar_movies": ["Inception", "Interstellar", "Blade Runner 2049"]
        },
        {
            "id": 108,
            "title": "Sicario",
            "release_date": "2015-09-18",
            "director": "Denis Villeneuve",
            "writers": ["Taylor Sheridan"],
            "producers": ["Basil Iwanyk", "Edward L. McDonnell"],
            "cinematographer": "Roger Deakins",
            "music_composer": "Jóhann Jóhannsson",
            "studio": "Lionsgate / Black Label Media",
            "awards": [],
            "trivia": [
                "Benicio del Toro came up with the idea to cut 90% of his character's dialogue to make him more mysterious.",
                "The border crossing sequence was filmed on a set replicating the real Juarez bridge, using 150 vehicles."
            ],
            "bts_facts": [
                "Roger Deakins used thermal and night-vision cameras for the tunnel ambush sequence, giving it an eerie tactical feel.",
                "The deep rumble in the soundtrack was composed by Jóhannsson to replicate the feeling of a heartbeat under stress."
            ],
            "cover_image": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=600&q=80",
            "similar_movies": ["Blade Runner 2049", "Oppenheimer", "Dune"]
        },

        # ── Letterboxd Top Films Catalog (with real TMDB posters) ──
        {
            "id": 1,
            "title": "The Godfather",
            "release_date": "1972-03-24",
            "director": "Francis Ford Coppola",
            "writers": ["Mario Puzo", "Francis Ford Coppola"],
            "producers": ["Albert S. Ruddy"],
            "cinematographer": "Gordon Willis",
            "music_composer": "Nino Rota",
            "studio": "Paramount Pictures",
            "awards": ["Academy Award for Best Picture", "Academy Award for Best Actor", "Academy Award for Best Adapted Screenplay"],
            "trivia": [
                "Marlon Brando stuffed his cheeks with cotton wool for his audition as Don Corleone.",
                "The cat held by Don Corleone in the opening scene was a stray found on set."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
            "similar_movies": ["Goodfellas", "The Godfather Part II"]
        },
        {
            "id": 2,
            "title": "The Shawshank Redemption",
            "release_date": "1994-09-23",
            "director": "Frank Darabont",
            "writers": ["Frank Darabont"],
            "producers": ["Niki Marvin"],
            "cinematographer": "Roger Deakins",
            "music_composer": "Thomas Newman",
            "studio": "Castle Rock Entertainment",
            "awards": [],
            "trivia": [
                "The film was a box office disappointment but became the most popular film on IMDb.",
                "Based on Stephen King's novella 'Rita Hayworth and Shawshank Redemption'."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
            "similar_movies": ["The Green Mile", "The Godfather"]
        },
        {
            "id": 3,
            "title": "Schindler's List",
            "release_date": "1993-11-30",
            "director": "Steven Spielberg",
            "writers": ["Steven Zaillian"],
            "producers": ["Steven Spielberg", "Gerald R. Molen", "Branko Lustig"],
            "cinematographer": "Janusz Kamiński",
            "music_composer": "John Williams",
            "studio": "Universal Pictures / Amblin Entertainment",
            "awards": ["Academy Award for Best Picture", "Academy Award for Best Director", "Academy Award for Best Cinematography"],
            "trivia": [
                "Steven Spielberg donated his entire directing fee to USC Shoah Foundation.",
                "Shot almost entirely in black and white, with the iconic red coat as the only color."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg",
            "similar_movies": ["The Pianist", "Life Is Beautiful"]
        },
        {
            "id": 4,
            "title": "Spirited Away",
            "release_date": "2001-07-20",
            "director": "Hayao Miyazaki",
            "writers": ["Hayao Miyazaki"],
            "producers": ["Toshio Suzuki"],
            "cinematographer": "Atsushi Okui",
            "music_composer": "Joe Hisaishi",
            "studio": "Studio Ghibli",
            "awards": ["Academy Award for Best Animated Feature"],
            "trivia": [
                "The film surpassed Titanic to become Japan's all-time highest-grossing film for 19 years.",
                "The spirit Haku is based on a real river that was paved over near Miyazaki's childhood home."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkQlXzZ0.jpg",
            "similar_movies": ["Princess Mononoke", "My Neighbor Totoro"]
        },
        {
            "id": 5,
            "title": "Parasite",
            "release_date": "2019-05-30",
            "director": "Bong Joon-ho",
            "writers": ["Bong Joon-ho", "Han Jin-won"],
            "producers": ["Bong Joon-ho", "Kwak Sin-ae"],
            "cinematographer": "Hong Kyung-pyo",
            "music_composer": "Jung Jae-il",
            "studio": "Barunson E&A",
            "awards": ["Academy Award for Best Picture", "Academy Award for Best Director", "Palme d'Or at Cannes"],
            "trivia": [
                "The first non-English film to win the Academy Award for Best Picture.",
                "Bong Joon-ho described the film as 'a comedy without clowns and a tragedy without villains'."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
            "similar_movies": ["Snowpiercer", "Memories of Murder"]
        },
        {
            "id": 6,
            "title": "The Dark Knight",
            "release_date": "2008-07-18",
            "director": "Christopher Nolan",
            "writers": ["Christopher Nolan", "Jonathan Nolan"],
            "producers": ["Emma Thomas", "Christopher Nolan", "Charles Roven"],
            "cinematographer": "Wally Pfister",
            "music_composer": "Hans Zimmer",
            "studio": "Warner Bros. Pictures",
            "awards": ["Academy Award for Best Supporting Actor (Heath Ledger)", "Academy Award for Best Sound Editing"],
            "trivia": [
                "Heath Ledger locked himself in a hotel room for six weeks to prepare for the Joker role.",
                "Ledger posthumously won the Academy Award for Best Supporting Actor."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            "similar_movies": ["Inception", "Oppenheimer"]
        },
        {
            "id": 7,
            "title": "12 Angry Men",
            "release_date": "1957-04-10",
            "director": "Sidney Lumet",
            "writers": ["Reginald Rose"],
            "producers": ["Henry Fonda", "Reginald Rose"],
            "cinematographer": "Boris Kaufman",
            "music_composer": "Kenyon Hopkins",
            "studio": "Orion-Nova Productions",
            "awards": [],
            "trivia": [
                "Shot entirely in one room, with the camera angles becoming increasingly claustrophobic as the film progresses.",
                "Nominated for three Academy Awards, including Best Picture."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg",
            "similar_movies": ["The Shawshank Redemption", "Schindler's List"]
        },
        {
            "id": 8,
            "title": "Pulp Fiction",
            "release_date": "1994-10-14",
            "director": "Quentin Tarantino",
            "writers": ["Quentin Tarantino", "Roger Avary"],
            "producers": ["Lawrence Bender"],
            "cinematographer": "Andrzej Sekula",
            "music_composer": "Various Artists",
            "studio": "Miramax Films",
            "awards": ["Academy Award for Best Original Screenplay", "Palme d'Or at Cannes"],
            "trivia": [
                "The film's non-linear timeline was inspired by time-hopping novels.",
                "John Travolta's career was revitalized by his role as Vincent Vega."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
            "similar_movies": ["Goodfellas", "The Dark Knight"]
        },
        {
            "id": 9,
            "title": "Forrest Gump",
            "release_date": "1994-07-06",
            "director": "Robert Zemeckis",
            "writers": ["Eric Roth"],
            "producers": ["Wendy Finerman", "Steve Tisch", "Steve Starkey"],
            "cinematographer": "Don Burgess",
            "music_composer": "Alan Silvestri",
            "studio": "Paramount Pictures",
            "awards": ["Academy Award for Best Picture", "Academy Award for Best Director", "Academy Award for Best Actor"],
            "trivia": [
                "Tom Hanks did not receive a salary for the film; he took percentage points instead, earning millions.",
                "The famous feather that opens and closes the film was digitally added in post-production."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
            "similar_movies": ["Cast Away", "The Shawshank Redemption"]
        },
        {
            "id": 10,
            "title": "The Matrix",
            "release_date": "1999-03-31",
            "director": "The Wachowskis",
            "writers": ["The Wachowskis"],
            "producers": ["Joel Silver"],
            "cinematographer": "Bill Pope",
            "music_composer": "Don Davis",
            "studio": "Warner Bros. / Village Roadshow",
            "awards": ["Academy Award for Best Visual Effects", "Academy Award for Best Film Editing"],
            "trivia": [
                "The 'bullet time' effect required 120 cameras to capture.",
                "Keanu Reeves learned all his fight choreography while recovering from neck surgery."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            "similar_movies": ["Inception", "Blade Runner 2049"]
        },
        {
            "id": 11,
            "title": "Goodfellas",
            "release_date": "1990-09-19",
            "director": "Martin Scorsese",
            "writers": ["Nicholas Pileggi", "Martin Scorsese"],
            "producers": ["Irwin Winkler"],
            "cinematographer": "Michael Ballhaus",
            "music_composer": "Various Artists",
            "studio": "Warner Bros. Pictures",
            "awards": ["Academy Award for Best Supporting Actor (Joe Pesci)"],
            "trivia": [
                "Joe Pesci's 'funny how?' scene was improvised based on a real-life incident he told Scorsese.",
                "The entire film spans 30 years of mob life from 1955 to 1984."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
            "similar_movies": ["The Godfather", "Pulp Fiction"]
        },
        {
            "id": 12,
            "title": "Seven Samurai",
            "release_date": "1954-04-26",
            "director": "Akira Kurosawa",
            "writers": ["Akira Kurosawa", "Shinobu Hashimoto", "Hideo Oguni"],
            "producers": ["Sojiro Motoki"],
            "cinematographer": "Asakazu Nakai",
            "music_composer": "Fumio Hayasaka",
            "studio": "Toho",
            "awards": [],
            "trivia": [
                "Inspired countless westerns, including The Magnificent Seven.",
                "The climactic rain-soaked battle sequence used water mixed with ink to make it more visible on camera."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/8OKmBV5NACo2O41b9TTC0aUqKz0.jpg",
            "similar_movies": ["The Godfather", "12 Angry Men"]
        },
        {
            "id": 13,
            "title": "City of God",
            "release_date": "2002-08-30",
            "director": "Fernando Meirelles",
            "writers": ["Bráulio Mantovani"],
            "producers": ["Andréa Barata Ribeiro", "Mauricio Andrade Ramos"],
            "cinematographer": "César Charlone",
            "music_composer": "Ed Cortês",
            "studio": "O2 Filmes",
            "awards": [],
            "trivia": [
                "The cast was primarily recruited from the favelas of Rio de Janeiro.",
                "Based on the semi-autobiographical novel by Paulo Lins."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/zpGvOa5X0rLgE22gYhD2iBf1JzH.jpg",
            "similar_movies": ["Parasite", "Goodfellas"]
        },
        {
            "id": 14,
            "title": "Se7en",
            "release_date": "1995-09-22",
            "director": "David Fincher",
            "writers": ["Andrew Kevin Walker"],
            "producers": ["Arnold Kopelson", "Phyllis Carlyle"],
            "cinematographer": "Darius Khondji",
            "music_composer": "Howard Shore",
            "studio": "New Line Cinema",
            "awards": [],
            "trivia": [
                "The script was considered so dark that the studio wanted to change the ending — Fincher refused.",
                "What's in the box? The film's ending remains one of cinema's most shocking."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/6yoghtyTpznpBik8EngEmJskVPh.jpg",
            "similar_movies": ["Sicario", "The Silence of the Lambs"]
        },
        {
            "id": 15,
            "title": "The Silence of the Lambs",
            "release_date": "1991-02-14",
            "director": "Jonathan Demme",
            "writers": ["Ted Tally"],
            "producers": ["Edward Saxon", "Kenneth Utt", "Ron Bozman"],
            "cinematographer": "Tak Fujimoto",
            "music_composer": "Howard Shore",
            "studio": "Orion Pictures",
            "awards": ["Academy Award for Best Picture", "Academy Award for Best Director", "Academy Award for Best Actor", "Academy Award for Best Actress"],
            "trivia": [
                "One of only three films to win all five major Academy Awards (Picture, Director, Actor, Actress, Screenplay).",
                "Anthony Hopkins is on screen for only 16 minutes despite winning Best Actor."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg",
            "similar_movies": ["Se7en", "Sicario"]
        },
        {
            "id": 16,
            "title": "Life Is Beautiful",
            "release_date": "1997-12-20",
            "director": "Roberto Benigni",
            "writers": ["Roberto Benigni", "Vincenzo Cerami"],
            "producers": ["Elda Ferri", "Gianluigi Braschi"],
            "cinematographer": "Tonino Delli Colli",
            "music_composer": "Nicola Piovani",
            "studio": "Melampo Cinematografica",
            "awards": ["Academy Award for Best Foreign Language Film", "Academy Award for Best Actor", "Academy Award for Best Original Dramatic Score"],
            "trivia": [
                "Roberto Benigni dedicated his Academy Award to his parents.",
                "The film was made in Italian and initially released in Europe before becoming an international hit."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/mfnkSeeVOBVheuyn2lo4tfmOPQb.jpg",
            "similar_movies": ["Schindler's List", "Forrest Gump"]
        },
        {
            "id": 17,
            "title": "Fight Club",
            "release_date": "1999-10-15",
            "director": "David Fincher",
            "writers": ["Jim Uhls"],
            "producers": ["Art Linson", "Ceán Chaffin", "Ross Grayson Bell"],
            "cinematographer": "Jeff Cronenweth",
            "music_composer": "The Dust Brothers",
            "studio": "Fox 2000 Pictures",
            "awards": [],
            "trivia": [
                "A single frame of an explicit image was spliced into the film near the end.",
                "Brad Pitt made Tyler Durden's appearance more intimidating by bleaching his hair and getting a tan."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
            "similar_movies": ["Pulp Fiction", "Se7en"]
        },
        {
            "id": 18,
            "title": "The Lord of the Rings: The Return of the King",
            "release_date": "2003-12-17",
            "director": "Peter Jackson",
            "writers": ["Fran Walsh", "Philippa Boyens", "Peter Jackson"],
            "producers": ["Peter Jackson", "Fran Walsh", "Barrie M. Osborne"],
            "cinematographer": "Andrew Lesnie",
            "music_composer": "Howard Shore",
            "studio": "New Line Cinema / WingNut Films",
            "awards": ["Academy Award for Best Picture", "Academy Award for Best Director", "11 Academy Awards total"],
            "trivia": [
                "Won all 11 Academy Awards it was nominated for — a joint record with Ben-Hur and Titanic.",
                "The film's runtime is 3 hours 21 minutes (201 minutes)."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5OUcvUUy.jpg",
            "similar_movies": ["The Lord of the Rings: The Fellowship of the Ring", "Dune"]
        },
        {
            "id": 19,
            "title": "The Lord of the Rings: The Fellowship of the Ring",
            "release_date": "2001-12-19",
            "director": "Peter Jackson",
            "writers": ["Fran Walsh", "Philippa Boyens", "Peter Jackson"],
            "producers": ["Peter Jackson", "Fran Walsh", "Barrie M. Osborne"],
            "cinematographer": "Andrew Lesnie",
            "music_composer": "Howard Shore",
            "studio": "New Line Cinema / WingNut Films",
            "awards": ["Academy Award for Best Cinematography", "Academy Award for Best Visual Effects"],
            "trivia": [
                "All three Lord of the Rings films were shot simultaneously over 14 months in New Zealand.",
                "Ian McKellen wept when he first read the script for Gandalf's 'You Shall Not Pass' scene."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
            "similar_movies": ["The Lord of the Rings: The Return of the King", "Dune"]
        },
        {
            "id": 20,
            "title": "Spider-Man: Into the Spider-Verse",
            "release_date": "2018-12-14",
            "director": "Bob Persichetti, Peter Ramsey, Rodney Rothman",
            "writers": ["Phil Lord", "Rodney Rothman"],
            "producers": ["Amy Pascal", "Phil Lord", "Christina Steinberg"],
            "cinematographer": "Justin K. Thompson",
            "music_composer": "Daniel Pemberton",
            "studio": "Sony Pictures Animation",
            "awards": ["Academy Award for Best Animated Feature"],
            "trivia": [
                "The animation style was designed to look like a moving comic book, with halftone dots and Ben-Day patterns.",
                "Miles Morales runs at 12 frames per second while established Spider-People run at 24, symbolizing his inexperience."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg",
            "similar_movies": ["Parasite", "The Dark Knight"]
        },
        {
            "id": 21,
            "title": "Avengers: Infinity War",
            "release_date": "2018-04-27",
            "director": "Anthony Russo, Joe Russo",
            "writers": ["Christopher Markus", "Stephen McFeely"],
            "producers": ["Kevin Feige"],
            "cinematographer": "Trent Opaloch",
            "music_composer": "Alan Silvestri",
            "studio": "Marvel Studios / Disney",
            "awards": ["Academy Award for Best Visual Effects"],
            "trivia": [
                "The Snap deleted half of all life in the universe — including half the film's cast.",
                "Josh Brolin wore a motion capture suit for Thanos and acted on set alongside other actors."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg",
            "similar_movies": ["The Dark Knight", "Spider-Man: Into the Spider-Verse"]
        },
        {
            "id": 22,
            "title": "The Usual Suspects",
            "release_date": "1995-08-16",
            "director": "Bryan Singer",
            "writers": ["Christopher McQuarrie"],
            "producers": ["Bryan Singer", "Michael McDonnell"],
            "cinematographer": "Newton Thomas Sigel",
            "music_composer": "John Ottman",
            "studio": "PolyGram Filmed Entertainment",
            "awards": ["Academy Award for Best Supporting Actor", "Academy Award for Best Original Screenplay"],
            "trivia": [
                "The lineup scene was improvised — the actors couldn't stop laughing at Benicio del Toro's flatulence.",
                "Keyser Söze's reveal is considered one of the greatest twist endings in cinema."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/rWgs151iJb2z8R1RMBV4uIDb3W3.jpg",
            "similar_movies": ["Se7en", "Pulp Fiction"]
        },
        {
            "id": 23,
            "title": "It's a Wonderful Life",
            "release_date": "1946-12-20",
            "director": "Frank Capra",
            "writers": ["Frances Goodrich", "Albert Hackett", "Frank Capra"],
            "producers": ["Frank Capra"],
            "cinematographer": "Joseph Walker",
            "music_composer": "Dimitri Tiomkin",
            "studio": "Liberty Films",
            "awards": [],
            "trivia": [
                "The film was originally a box office disappointment but became beloved through decades of TV reruns.",
                "The snow used in the film was revolutionary — it was aluminum powder and foamite."
            ],
            "bts_facts": [],
            "cover_image": "https://image.tmdb.org/t/p/w500/bSqt9rhDZx1Q7UZ86dBPKdNomp2.jpg",
            "similar_movies": ["Forrest Gump", "Schindler's List"]
        },
    ]

    for m in movies_data:
        movie = Movie(**m)
        session.add(movie)

    # --- POPULATE A DEFAULT TEST USER ---
    # Password: tyler (hash generated via standard PBKDF2)
    # Salt: leesure_salt
    # Hash value: PBKDF2 with SHA256
    import hashlib
    dk = hashlib.pbkdf2_hmac('sha256', b'tyler', b'leesure_salt', 100000)
    password_hash = "pbkdf2_sha256$100000$leesure_salt$" + dk.hex()

    user = User(
        username="demo",
        password_hash=password_hash,
        rank="Observer",
        xp=0,
        profile_cosmetics=["Default Violet Glow", "Minimalist Gray"]
    )
    session.add(user)

    session.commit()
    print("Database seeded successfully with games, movies, and demo user!")
    session.close()

if __name__ == "__main__":
    seed_database()
