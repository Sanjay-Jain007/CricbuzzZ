import requests
import sqlite3
import time

API_KEY = "YOUR_RAPIDAPI_KEY"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

conn = sqlite3.connect("cricbuzz.db")
cursor = conn.cursor()

# --------------------------------------------------
# Get recent matches
# --------------------------------------------------

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

response = requests.get(url, headers=headers)
data = response.json()

match_ids = []

for match_type in data.get("typeMatches", []):
    for series in match_type.get("seriesMatches", []):

        wrapper = series.get("seriesAdWrapper")

        if wrapper:

            for match in wrapper.get("matches", []):

                match_id = match["matchInfo"]["matchId"]
                match_ids.append(match_id)

# Limit to 100 matches
match_ids = match_ids[:100]

print("Matches found:", len(match_ids))

# --------------------------------------------------
# Fetch scorecards
# --------------------------------------------------

for match_id in match_ids:

    score_url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"

    score_response = requests.get(score_url, headers=headers)

    if score_response.status_code != 200:
        continue

    score_data = score_response.json()

    for inning in score_data.get("scoreCard", []):

        # Batting stats
        for batsman in inning.get("batTeamDetails", {}).get("batsmenData", {}).values():

            name = batsman.get("batName")
            runs = batsman.get("runs", 0)

            if name:

                cursor.execute(
                    "INSERT INTO players (full_name) VALUES (?)",
                    (name,)
                )

                player_id = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO batting_stats (player_id, match_id, runs) VALUES (?, ?, ?)",
                    (player_id, match_id, runs)
                )

        # Bowling stats
        for bowler in inning.get("bowlTeamDetails", {}).get("bowlersData", {}).values():

            name = bowler.get("bowlName")
            wickets = bowler.get("wickets", 0)

            if name and wickets > 0:

                cursor.execute(
                    "INSERT INTO players (full_name) VALUES (?)",
                    (name,)
                )

                player_id = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO bowling_stats (player_id, match_id, wickets) VALUES (?, ?, ?)",
                    (player_id, match_id, wickets)
                )

    print("Processed match:", match_id)

    time.sleep(1)

conn.commit()
conn.close()

print("Database updated with real match statistics")
