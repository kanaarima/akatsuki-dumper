import sqlite3
import config

db = sqlite3.connect(config.PARENT+"/database.db")

USERS = """
CREATE TABLE "users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL,
	"username_aka"	TEXT NOT NULL,
	"registered_on"	TEXT NOT NULL,
	"privileges"	INTEGER NOT NULL,
	"latest_activity"	TEXT NOT NULL,
	"country"	TEXT NOT NULL,
	"play_style"	INTEGER NOT NULL,
	"favourite_mode"	INTEGER NOT NULL,
	"followers"	INTEGER NOT NULL,
	"badges"	TEXT NOT NULL,
	"tbadges"	TEXT NOT NULL,
	"custom_badge"	TEXT NOT NULL,
	"silence_info"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
"""
BADGES = """CREATE TABLE "badges" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"icon"	TEXT NOT NULL,
	PRIMARY KEY("id")
)"""

CLANS = """CREATE TABLE "clans" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"tag"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"icon"	TEXT NOT NULL,
	"owner"	INTEGER NOT NULL,
	"status"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);"""

BEATMAPS = """CREATE TABLE "beatmaps" (
	"beatmap_id"	INTEGER NOT NULL UNIQUE,
	"beatmapset_id"	INTEGER NOT NULL,
	"beatmap_md5"	TEXT NOT NULL,
	"song_name"	TEXT NOT NULL,
	"ar"	REAL NOT NULL,
	"od"	REAL NOT NULL,
	"difficulty"	REAL NOT NULL,
	"max_combo"	INTEGER NOT NULL,
	"hit_length"	INTEGER NOT NULL,
	"ranked"	INTEGER NOT NULL,
	"ranked_status_freezed"	INTEGER NOT NULL,
	"latest_update"	TEXT NOT NULL,
	PRIMARY KEY("beatmap_id")
);"""

USER_STATS = """CREATE TABLE "user_stats" (
	"user_id"	INTEGER NOT NULL,
	"mode"	INTEGER NOT NULL,
	"relax"	INTEGER NOT NULL,
	"ranked_score"	INTEGER NOT NULL,
	"total_score"	INTEGER NOT NULL,
	"playcount"	INTEGER NOT NULL,
	"playtime"	INTEGER NOT NULL,
	"replays_watched"	INTEGER NOT NULL,
	"total_hits"	INTEGER NOT NULL,
	"level"	REAL NOT NULL,
	"accuracy"	REAL NOT NULL,
	"pp"	INTEGER NOT NULL,
	"global_leaderboard_rank"	INTEGER NOT NULL,
	"country_leaderboard_rank"	INTEGER NOT NULL,
	"max_combo"	INTEGER NOT NULL,
	PRIMARY KEY("user_id","mode","relax")
);"""

USER_MOST_PLAYED = """CREATE TABLE "user_most_played" (
	"user_id"	INTEGER NOT NULL,
	"mode"	INTEGER NOT NULL,
	"relax"	INTEGER NOT NULL,
	"beatmap_id"	INTEGER NOT NULL,
	"playcount"	INTEGER NOT NULL
);"""

USER_SCORES = """CREATE TABLE "user_scores" (
	"user_id"	INTEGER NOT NULL,
	"mode"	INTEGER NOT NULL,
	"relax"	INTEGER NOT NULL,
	"beatmap_md5"	TEXT NOT NULL,
	"score"	INTEGER NOT NULL,
	"max_combo"	INTEGER NOT NULL,
	"full_combo"	INTEGER NOT NULL,
	"mods"	INTEGER NOT NULL,
	"count_300"	INTEGER NOT NULL,
	"count_100"	INTEGER NOT NULL,
	"count_50"	INTEGER NOT NULL,
	"count_geki"	INTEGER NOT NULL,
	"count_katu"	INTEGER NOT NULL,
	"count_miss"	INTEGER NOT NULL,
	"time"	TEXT NOT NULL,
	"accuracy"	REAL NOT NULL,
	"pp"	REAL NOT NULL,
	"rank"	TEXT NOT NULL,
	"completed"	INTEGER NOT NULL,
	"pinned"	INTEGER NOT NULL
);"""

USER_PINNED = """CREATE TABLE "user_pinned" (
	"user_id"	INTEGER NOT NULL,
	"mode"	INTEGER NOT NULL,
	"relax"	INTEGER NOT NULL,
	"beatmap_md5"	TEXT NOT NULL,
	"score"	INTEGER NOT NULL,
	"max_combo"	INTEGER NOT NULL,
	"full_combo"	INTEGER NOT NULL,
	"mods"	INTEGER NOT NULL,
	"count_300"	INTEGER NOT NULL,
	"count_100"	INTEGER NOT NULL,
	"count_50"	INTEGER NOT NULL,
	"count_geki"	INTEGER NOT NULL,
	"count_katu"	INTEGER NOT NULL,
	"count_miss"	INTEGER NOT NULL,
	"time"	TEXT NOT NULL,
	"accuracy"	REAL NOT NULL,
	"pp"	REAL NOT NULL,
	"rank"	TEXT NOT NULL,
	"completed"	INTEGER NOT NULL,
	"pinned"	INTEGER NOT NULL
);"""

USER_FIRST_PLACES = """CREATE TABLE "user_first_places" (
	"user_id"	INTEGER NOT NULL,
	"mode"	INTEGER NOT NULL,
	"relax"	INTEGER NOT NULL,
	"beatmap_md5"	TEXT NOT NULL,
	"score"	INTEGER NOT NULL,
	"max_combo"	INTEGER NOT NULL,
	"full_combo"	INTEGER NOT NULL,
	"mods"	INTEGER NOT NULL,
	"count_300"	INTEGER NOT NULL,
	"count_100"	INTEGER NOT NULL,
	"count_50"	INTEGER NOT NULL,
	"count_geki"	INTEGER NOT NULL,
	"count_katu"	INTEGER NOT NULL,
	"count_miss"	INTEGER NOT NULL,
	"time"	TEXT NOT NULL,
	"accuracy"	REAL NOT NULL,
	"pp"	REAL NOT NULL,
	"rank"	TEXT NOT NULL,
	"completed"	INTEGER NOT NULL,
	"pinned"	INTEGER NOT NULL
);"""

USER_LEADERBOARDS = """CREATE TABLE "user_leaderboard" (
	"user_id"	INTEGER NOT NULL,
	"mode"	INTEGER NOT NULL,
	"relax"	INTEGER NOT NULL,
	"position"	INTEGER NOT NULL
);"""


def create_database():
    db.execute("pragma journal_mode=wal")
    queries = [USERS, USER_SCORES, USER_STATS, USER_MOST_PLAYED, USER_FIRST_PLACES, USER_PINNED, USER_LEADERBOARDS, BADGES, CLANS, BEATMAPS]
    for query in queries:
        db.execute(query)
