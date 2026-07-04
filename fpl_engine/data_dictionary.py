bootstrap_static_elements_data_dictionary = {
    "information" : "one row per player, current snapshot", 
    "element_type": "Position: 1 = GK, 2 = DEF, 3 = MID, 4 = FWD",
    "now_cost" : "Current price x 10 - divide by 10 for £m (e.g. 125 = £12.5m)",
    "total_points" : "Season-to-date points",
    "bps" : "Total bonus points system score (raw, pre-bonus-allocation)", 
    "ict_index" : "FPL's own form/quality metric", 
    "selected_by percent" : "ownership percent across all FPL managers", 
    "transfers_in_event, transfers_out_event" : "Just this gameweek - more useful for price-change prediction",
    "transfers_in, transfers_out" : "season totals",
    "status" : "a=availaible, i=injured, d=doubtful, s=suspended, u=unavailable",
    "value_season" : "Points per £m spent — a value efficiency metric"
}

player_summary_data_dictionary = {
    "information" : "one row per player per past gameweek",
    "round": "gameweek number",
    "total_points" : "Points scored that GW — your prediction target",
    "selected" : "Absolute ownership count (notpercent) that GW"
}

fixtures_data_dictionary = {
    "information" : "data on all the fixtures",
    "event" : "Gameweek number",
    "team_h_difficulty, team_a_difficulty" : "FPL's own 1-5 FDR rating",
    "team_h_score, team_a_score" : "Null if not yet played",
    "finished" : "Whether the match has completed"
}