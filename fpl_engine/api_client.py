import requests
import json
import time
from pathlib import Path

"""
bootstrap-static/ : All players, teams, gameweek schedule, current prices
fixtures/ : Every match with FDR (Fixture difficulty rating)
element-summary/{id}/ : Full per player history by gameweek
event/{gw}/live/ : Live bonus points, actual minutes played
"""

BASE_URL = "https://fantasy.premierleague.com/api"
RAW_DIR = Path(__file__).parent.parent / "Data" / "raw"

def fetch_bootstrap():
    """
    The master endpoint. Returns every player, team, gameweek, and
    current prices in one call.
    """
    url = f"{BASE_URL}/bootstrap-static/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(RAW_DIR / "bootstrap.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Fetched {len(data['elements'])} players")
    print(f"Fetched {len(data['teams'])} teams")
    return data

def fetch_fixtures():
    """
    All fixtures for the season with FDR (Fixture difficulty data) scores.
    """
    url = f'{BASE_URL}/fixtures'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    with open(RAW_DIR / "fixtures.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Fetched {len(data)} fixtures")
    return data

def fetch_player_history(player_id: int):
    """
    Per-player historical stats broken down by gameweek
    This is where actual points, minutes, xG etc. live
    """
    url=f"{BASE_URL}/element-summary/{player_id}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def load_bootstrap():
    with open(RAW_DIR / "bootstrap.json") as f:
        data = json.load(f)
        print(f"Loaded {len(data["elements"])} players")
        print(f"Loaded {len(data["teams"])} teams")
        return data

    

def load_fixtures():
    with open(RAW_DIR / "fixtures.json") as f:
        data = json.load(f)
        print(f"Loaded {len(data)} fixtures")
        return data

def load_player_history(player_id: int):
    with open(RAW_DIR / "players" / f"{player_id}.json") as f:
        return json.load(f)

def fetch_all_player_histories(player_ids: list):
    """
    Loops over every player and saves their history. 
    Includes a delay to avoid hammering the API
    """
    players_dir = RAW_DIR / "players"
    players_dir.mkdir(parents=True, exist_ok=True)

    # i tracks iteration index and pid  tracked item itself within player_ids
    for i, pid in enumerate(player_ids):
        filepath = players_dir / f"{pid}.json"

        if filepath.exists():
            continue

        data = fetch_player_history(pid)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        time.sleep(0.5)

        if i % 50 == 0:
            print(f" {i}/{len(player_ids)} players fetched...")

    print("Done - all player histories saved")
