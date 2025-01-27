"""
    Future Databank - when the game gets bigger :)
"""

# import sqlite3
# import os
# import random


# current_dir = os.path.dirname(os.path.abspath(__file__))
# db_name = "words.db"


# db_path = os.path.join(current_dir, db_name)

# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# cursor.execute(
#     """
#     CREATE  TABLE IF NOT EXISTS words (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     word TEXT NOT NULL UNIQUE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )    
#     """
# )

# conn.commit()
# conn.close()


# # Add words
# def add_words(word):
#     conn = sqlite3.connect("words.db")
#     cursor = conn.cursor()

#     try:
#         cursor.execute("INSERT INTO words (word) VALUES (?)", (word,))
#         conn.commit()
#         print(f"'{word}' added successfully!")
#     except sqlite3.IntegrityError:
#         print(f"This word '{word}' already exists!")
#     finally:
#         conn.close()


# # Add Words through method
# def add_words_from_list(word_list):
#     for word in word_list:
#         add_words(word)

word_list = [
        "Dragon",
        "Oracle",
        "Quest",
        "Frostbite",
        "Aurora",
        "Paradox",
        "Illusion",
        "Labyrinth",
        "Eclipse",
        "Cryptic",
        "Enigma",
        "Whisper",
        "Echo",
        "Phantom",
        "Mysterious",
        "Ocean",
        "Mountain",
        "Chocolate",
        "Tennis",
        "Butterfly",
        "Candle",
        "Music",
        "Cloud",
        "Tornado",
        "Puzzle"
]

