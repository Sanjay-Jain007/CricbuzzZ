import requests
import sqlite3

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

headers = {
    "X-RapidAPI-Key": "YOUR_API_KEY",
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data = response.json()

conn = sqlite3.connect("cricbuzz.db")
cursor = conn.cursor()

for match_type in data.get("typeMatches", []):
    for series in match_type.get("seriesMatches", []):

        wrapper = series.get("seriesAdWrapper")

        if wrapper:

            for match in wrapper.get("matches", []):

                info = match.get("matchInfo", {})
                score = match.get("matchScore", {})

                team1 = info.get("team1", {}).get("teamName")
                team2 = info.get("team2", {}).get("teamName")

                if "team1Score" in score:

                    runs = score["team1Score"]["inngs1"].get("runs", 0)

                    cursor.execute(
                        "INSERT INTO players (full_name) VALUES (?)",
                        (team1,)
                    )

                    player_id = cursor.lastrowid

                    cursor.execute(
                        "INSERT INTO batting_stats (player_id, match_id, runs) VALUES (?,?,?)",
                        (player_id, 1, runs)
                    )

conn.commit()
conn.close()

print("Database updated with real match data")
