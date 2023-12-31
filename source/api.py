from config import REQUEST_DELAY
from enum import Enum
from typing import *
import requests
import time

class GamemodeString(Enum):
    std = 0
    taiko = 1
    ctb = 2
    mania = 3

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

class Beatmap(TypedDict):
    beatmap_id: int
    beatmapset_id: int
    beatmap_md5: str
    song_name: str
    ar: float
    od: float
    difficulty: float # super broken
    difficulty2: Dict[GamemodeString, float] # same
    max_combo: int
    hit_length: int
    ranked: int
    ranked_status_freezed: int
    latest_update: str

class Badge(TypedDict):
    id: int
    name: str
    icon: str

class SilenceInfo(TypedDict):
    reason: str
    end: str

class Clan(TypedDict):
    id: int
    name: str
    tag: str
    description: str
    icon: str
    owner: int
    status: int

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
    stats: List[Dict[GamemodeString, ChosenMode]]
    followers: int
    clan: Clan
    badges: List[Badge]
    tbadges: List[Badge]
    custom_badge: Badge
    silence_info: SilenceInfo

class Score(TypedDict):
    id: str # not a bug
    beatmap_md5: str
    score: int
    max_combo: int
    full_combo: bool
    mods: int
    count_300: int
    count_100: int
    count_50: int
    count_geki: int
    count_katu: int
    count_miss: int
    time: str
    play_mode: int
    accuracy: float
    pp: float
    rank: Union[str, int] # ???
    completed: int
    pinned: bool
    beatmap: Beatmap

class MostPlayedMap(TypedDict):
    playcount: int
    beatmap: Beatmap

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
    country_rank = {}
    rank = 0
    def get_country_rank(country):
        if country not in country_rank:
            country_rank[country] = 0
        country_rank[country] += 1
        return country_rank[country]
    while True:
        print(f"Crawling page {page} (current users found: {len(res)})")
        req = get(f"https://akatsuki.gg/api/v1/leaderboard?mode={mode}&p={page}&l=500&rx={relax}&sort=magic")
        if not req:
            break
        if not req['users']:
            break
        for user in req['users']:
            rank+=1
            chosen_mode = user['chosen_mode']
            del user['chosen_mode']
            user_dict = initialise_dict(user, User)
            chosen_mode_dict = initialise_dict(chosen_mode, ChosenMode)
            chosen_mode_dict['global_leaderboard_rank'] = rank
            chosen_mode_dict['country_leaderboard_rank'] = get_country_rank(user_dict['country'])
            if non_zero_dict(chosen_mode_dict, ignore_keys=["level", "global_leaderboard_rank", "country_leaderboard_rank"]):
                res.append((user_dict, chosen_mode_dict))
            else:
                print("Found empty user, breaking")
                return res
        page +=1
        time.sleep(REQUEST_DELAY)
    return res

def get_user_info(user_id: int) -> User:
    req = get(f"https://akatsuki.gg/api/v1/users/full?id={user_id}")
    if not req:
        return
    del req['code']
    return initialise_dict(req, User)

def get_user_pinned(user_id: int, mode=0, relax=0) -> List[Score]:
    res = list()
    page = 1
    while True:
        req = get(f"https://akatsuki.gg/api/v1/pinned/pinned?mode={mode}&p={page}&l=100&rx={relax}&id={user_id}")
        if not req or not req['scores']:
            break
        for score in req['scores']:
            res.append(initialise_dict(score, Score))
        page+=1
    return res

def get_user_most_played(user_id: int, mode=0, relax=0) -> List[MostPlayedMap]:
    res = list()
    page = 1
    while True:
        req = get(f"https://akatsuki.gg/api/v1/users/most_played?mode={mode}&p={page}&l=100&rx={relax}&id={user_id}")
        if not req or not req['most_played_beatmaps']:
            break
        for maps in req['most_played_beatmaps']:
            res.append(initialise_dict(maps, MostPlayedMap))
        page+=1
    return res

def get_user_best(user_id: int, mode=0, relax=0) -> List[Score]:
    res = list()
    page = 1
    while True:
        req = get(f"https://akatsuki.gg/api/v1/users/scores/best?mode={mode}&p={page}&l=100&rx={relax}&id={user_id}")
        if not req or not req['scores']:
            break
        for score in req['scores']:
            res.append(initialise_dict(score, Score))
        page+=1
    return res

def get_user_first_places(user_id: int, mode=0, relax=0) -> List[Score]:
    res = list()
    page = 1
    while True:
        req = get(f"https://akatsuki.gg/api/v1/users/scores/first?mode={mode}&p={page}&l=100&rx={relax}&id={user_id}")
        if not req or not req['scores']:
            break
        for score in req['scores']:
            res.append(initialise_dict(score, Score))
        page+=1
    return res
