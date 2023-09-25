from typing import *
import config
import json
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
    while True:
        pass

tasks: Dict[str, callable] = {"store_leaderboards": store_leaderboards}

if __name__ == "__main__":
    os.makedirs(config.PARENT,exist_ok=True)
    session = load_previous_session(config.PARENT)
    is_null = session["task_name"] is None
    if not is_null:
        print("Resuming session: " + session["task_name"])
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
    except KeyboardInterrupt:
        print("Saving current session...")
        with open(config.PARENT+"/session.json", "w") as f:
            json.dump(session, f)
