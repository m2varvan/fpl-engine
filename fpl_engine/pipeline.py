import json
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "Data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "Data" / "processed"

def build_raw_modelling_feature_store():
    # Grab the position data, team data, name for each player and put it into a dataframe
    with open(RAW_DIR / "bootstrap.json") as f:
        data = json.load(f)
    
    players_data = pd.DataFrame(data['elements'])
    players_data = players_data[['id', 'team', 'element_type', 'web_name']].rename(columns={"id": "player_id", "element_type": "position"})

    team_names = {team["id"]: team["name"] for team in data["teams"]}

    # Grab the fixture data
    with open(RAW_DIR / "fixtures.json") as f:
        data = json.load(f)

    fixture_data = pd.DataFrame(data)[["id", "team_h_difficulty", "team_a_difficulty"]]
    fixture_data = fixture_data.rename(columns={"id": "fixture_id"})

    # Loop through every players history and stack into one table
    all_rows = []
    players_dir = RAW_DIR / "players"

    # glob("*.json") finds all files like : 381.json, 254.json, 17.json
    for filepath in players_dir.glob("*.json"):
        with open(filepath) as f:
            data = json.load(f)
        
        history = data.get("history", [])
        if not history:
            continue

        for row in history:
            all_rows.append({
                # Context
                "player_id": row["element"],
                "gameweek": row["round"],
                "fixture_id": row["fixture"],
                "was_home": row["was_home"],
                "opponent_team": row["opponent_team"],
                # Playing time
                "starts": row["starts"],
                "minutes": row["minutes"],
                # Market
                "price": row["value"] / 10,
                "selected": row["selected"],
                "transfers_in": row["transfers_in"],
                "transfers_out": row["transfers_out"],
                # Outcome
                "total_points": row["total_points"],
                "bonus": row["bonus"],
                "bps": row["bps"],
                # Attacking stats
                "goals_scored": row["goals_scored"],
                "assists": row["assists"],
                "ict_index": float(row["ict_index"]),
                # Defensive stats
                "clean_sheets": row["clean_sheets"],
                "goals_conceded": row["goals_conceded"],
                "saves": row["saves"],
                "defensive_contribution": row["defensive_contribution"],
                # Expected stats
                "expected_goals": float(row["expected_goals"]),
                "expected_assists": float(row["expected_assists"]),
                "expected_goal_involvements": float(row["expected_goal_involvements"]),
                "expected_goals_conceded": float(row["expected_goals_conceded"]),
            })
    
    df = pd.DataFrame(all_rows)

    # merging the two dataframes on player id and fixture id
    df = pd.merge(df, players_data, on="player_id", how="left", validate="many_to_one")
    df = pd.merge(df, fixture_data, on="fixture_id", how="left", validate="many_to_one")

    # Add difficulty column
    df["difficulty"] = df.apply(
        lambda row: row["team_h_difficulty"] if row["was_home"]
        else row["team_a_difficulty"],
        axis=1
    )
    df = df.drop(columns=['team_h_difficulty', 'team_a_difficulty'])

    # Map team IDs to readable names
    df["team_name"] = df["team"].map(team_names)
    df["opponent_team_name"] = df["opponent_team"].map(team_names)


    # Sort the data by player then gameweek
    df = df.sort_values(["player_id", "gameweek"]).reset_index(drop=True)
    
    # Save
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PROCESSED_DIR / "raw_modelling_feature_store.parquet", index=False)

    print(f"Feature store built: {df.shape[0]} rows, {df.shape[1]} cols")
    print(f"Players: {df['player_id'].nunique()}")
    print(f"Gameweeks: {df['gameweek'].min()} – {df['gameweek'].max()}")
    print(f"Fixtures: {df['fixture_id'].nunique()}")
    
    return df

if __name__ == "__main__":
    build_raw_modelling_feature_store()


