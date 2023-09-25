from typing import *
import database
import config
import json
import api
import os

class Session(TypedDict):
    task_name: str
    current_data: object

def load_previous_session(parent: str) -> Session:
    if os.path.exists(parent+"/session.json"):
        with open(parent+"/session.json") as f:
            return json.load(f)
    return Session(task_name=None, current_data=None)

def store_leaderboards(session: Session):
    modes = [[0,1,2,3],[0,1,2],[0]]
    cur = database.db.cursor()
    for rx in range(3):
        for mode in modes[rx]:
            leaderboard = api.get_leaderboard(mode=mode, relax=rx)
            for user, chosen_mode in leaderboard:
                cur.execute("INSERT OR IGNORE INTO user_leaderboard VALUES (?,?,?,?)", (user["id"], mode, rx, chosen_mode["global_leaderboard_rank"]))
                cur.execute("INSERT OR IGNORE INTO user_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    user["id"], mode, rx, chosen_mode["ranked_score"], chosen_mode["total_score"], chosen_mode['playcount'], chosen_mode['playtime'], chosen_mode['replays_watched'], chosen_mode["total_hits"], chosen_mode['level'], chosen_mode["accuracy"], chosen_mode["pp"], chosen_mode["global_leaderboard_rank"], chosen_mode["country_leaderboard_rank"], chosen_mode['max_combo']
                ))
                database.db.commit()

def store_users(session:Session):
    modes = [[0,1,2,3],[0,1,2],[0]]
    skip_to = None
    if session["current_data"]:
        skip_to = session["current_data"]
    cur = database.db.cursor()
    users = cur.execute("SELECT DISTINCT user_id FROM user_stats").fetchall()
    current = 0
    for rows in users:
        current += 1
        user_id = rows[0]
        if skip_to:
            if user_id != skip_to:
                continue
            else:
                skip_to = None
        session['current_data'] = user_id
        user = api.get_user_info(user_id)
        print(f"Processing user {current}/{len(users)}: {user['username']}")
        badges = ""
        if user['badges']: # TODO: store badges
            badges = ','.join(str(badge['name']) for badge in user['badges'])
        tbadges = ""
        if user['tbadges']:
            tbadges = ','.join(str(badge['name']) for badge in user['tbadges'])
        custom_badge = user['custom_badge']["name"] if user['custom_badge'] else ""
        cur.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            user_id, user['username'], user["username_aka"], user['registered_on'], user['privileges'], user['latest_activity'], user['country'], user['play_style'], user['favourite_mode'], user['followers'], badges, tbadges, custom_badge, user['silence_info']["reason"]
        ))
        for rx in range(3):
            for mode in modes[rx]:
                print(f"processing mode {mode}+{rx}")
                print("getting pinned scores...")
                pinned = api.get_user_pinned(user_id=user_id, mode=mode, relax=rx)
                print("getting first places...")
                first_places = api.get_user_first_places(user_id=user_id, mode=mode, relax=rx)
                print("getting best plays...")
                best_plays = api.get_user_best(user_id=user_id, mode=mode, relax=rx)
                print("getting most played...")
                most_played = api.get_user_most_played(user_id=user_id, mode=mode, relax=rx)
                print(f"storing... (pinned: {len(pinned)}, #1: {len(first_places)}, clears: {len(best_plays)}, most played: {len(most_played)})")
                for score in pinned:
                    cur.execute("INSERT OR REPLACE INTO user_pinned VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        user_id, mode, rx, score['beatmap_md5'], score['score'], score['max_combo'], 1 if score['full_combo'] else 0, score['mods'], score['count_300'], score['count_100'], score['count_50'], score['count_geki'], score['count_katu'], score['count_miss'], score["time"], score['accuracy'], score['pp'], score['rank'],score["completed"], 1
                    ))
                    beatmap = score['beatmap']
                    cur.execute("INSERT OR REPLACE INTO beatmaps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        beatmap['beatmap_id'], beatmap['beatmapset_id'], beatmap['beatmap_md5'], beatmap['song_name'], beatmap['ar'], beatmap['od'], beatmap['difficulty'], beatmap['max_combo'], beatmap['hit_length'], beatmap['ranked'], beatmap['ranked_status_freezed'], beatmap['latest_update']
                    ))
                for score in first_places:
                    cur.execute("INSERT OR REPLACE INTO user_first_places VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        user_id, mode, rx, score['beatmap_md5'], score['score'], score['max_combo'], 1 if score['full_combo'] else 0, score['mods'], score['count_300'], score['count_100'], score['count_50'], score['count_geki'], score['count_katu'], score['count_miss'], score["time"], score['accuracy'], score['pp'], score['rank'],score["completed"], 1 if score['pinned'] else 0
                    ))
                    beatmap = score['beatmap']
                    cur.execute("INSERT OR IGNORE INTO beatmaps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        beatmap['beatmap_id'], beatmap['beatmapset_id'], beatmap['beatmap_md5'], beatmap['song_name'], beatmap['ar'], beatmap['od'], beatmap['difficulty'], beatmap['max_combo'], beatmap['hit_length'], beatmap['ranked'], -1000, beatmap['latest_update']
                    ))
                for score in best_plays:
                    cur.execute("INSERT OR REPLACE INTO user_scores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        user_id, mode, rx, score['beatmap_md5'], score['score'], score['max_combo'], 1 if score['full_combo'] else 0, score['mods'], score['count_300'], score['count_100'], score['count_50'], score['count_geki'], score['count_katu'], score['count_miss'], score["time"], score['accuracy'], score['pp'], score['rank'],score["completed"], 1 if score['pinned'] else 0
                    ))
                    beatmap = score['beatmap']
                    cur.execute("INSERT OR IGNORE INTO beatmaps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        beatmap['beatmap_id'], beatmap['beatmapset_id'], beatmap['beatmap_md5'], beatmap['song_name'], beatmap['ar'], beatmap['od'], beatmap['difficulty'], beatmap['max_combo'], beatmap['hit_length'], beatmap['ranked'], -1000, beatmap['latest_update']
                    ))
                for map in most_played:
                    cur.execute("INSERT OR REPLACE INTO user_most_played VALUES (?,?,?,?,?)", (
                        user_id, mode, rx, map['beatmap']['beatmap_id'], map['playcount']
                    ))
                    beatmap = map['beatmap']
                    cur.execute("INSERT OR IGNORE INTO beatmaps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        beatmap['beatmap_id'], beatmap['beatmapset_id'], beatmap['beatmap_md5'], beatmap['song_name'], beatmap['ar'], beatmap['od'], beatmap['difficulty'], beatmap['max_combo'], beatmap['hit_length'], beatmap['ranked'], -100, beatmap['latest_update']
                    ))
        database.db.commit()
tasks: Dict[str, callable] = {"store_leaderboards": store_leaderboards, "store_users": store_users}

if __name__ == "__main__":
    os.makedirs(config.PARENT,exist_ok=True)
    session = load_previous_session(config.PARENT)
    is_null = session["task_name"] is None
    if not is_null:
        print("Resuming session: " + session["task_name"])
    else:
        database.create_database()
    try:
        for task_name in tasks:
            if is_null:
                print("Running task " + task_name)
                session["task_name"] = task_name
                session["current_data"] = None
                tasks[task_name](session)
            else:
                if session["task_name"] == task_name:
                    print("Running task " + task_name)
                    tasks[task_name](session)
                    is_null = True
    except KeyboardInterrupt or Exception as e:
        if type(e) != KeyboardInterrupt:
            print(e)
        print("Saving current session...")
        with open(config.PARENT+"/session.json", "w") as f:
            json.dump(session, f)
