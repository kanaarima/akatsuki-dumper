from typing import TypedDict, List, Tuple
from config import REQUEST_DELAY
import requests
import time

class User(TypedDict):
    id: int
    username: str
    username_aka: str
    registered_on: str
    privileges: int
    latest_activity: str
    country: str
    play_style: int
    favourite_mode: int

class ChosenMode(TypedDict):
    ranked_score: int
    total_score: int
    playcount: int
    playtime: int
    replays_watched: int
    total_hits: int
    level: float
    accuracy: float
    pp: int
    global_leaderboard_rank: int
    country_leaderboard_rank: int
    max_combo: int

def initialise_dict(data, typed_dict: TypedDict):
    result = typed_dict()
    for key in data:
        if key not in typed_dict.__annotations__:
            print(f"{key} not found on {typed_dict.__class__.__name__}!")
        else:
            result[key] = data[key]
    return result

def non_zero_dict(dict: dict, ignore_keys: list = []):
    for key in dict:
        if key in ignore_keys:
            continue
        if dict[key]:
            return True
    return False

def get(url):
    req = requests.get(url)
    # TODO: log requests
    if req.ok:
        return req.json()

def get_leaderboard(mode=0, relax=0) -> List[Tuple[User, ChosenMode]]:
    res = list()
    page = 1
    while True:
        print(f"Crawling page {page} (current users found: {len(res)})")
        req = get(f"https://akatsuki.gg/api/v1/leaderboard?mode={mode}&p={page}&l=500&rx={relax}&sort=magic")
        if not req:
            break
        if not req['users']:
            break
        for user in req['users']:
            chosen_mode = user['chosen_mode']
            del user['chosen_mode']
            user_dict = initialise_dict(user, User)
            chosen_mode_dict = initialise_dict(chosen_mode, ChosenMode)
            if non_zero_dict(chosen_mode_dict, ignore_keys=["level"]):
                res.append((user_dict, chosen_mode_dict))
            else:
                print("Found empty user, breaking")
                return res
        page +=1
        time.sleep(REQUEST_DELAY)
    return res