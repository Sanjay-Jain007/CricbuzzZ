import json
import os
import sqlite3

data_folder = "cricsheet_data"

conn = sqlite3.connect("cricbuzz.db")
cursor = conn.cursor()

players = set()

for file in os.listdir(data_folder):
    if file.endswith(".json"):
        path = os.path.join(data_folder, file)

        with open(path) as f:
            data = json.load(f)

            if "players" in data["info"]:
                for team in data["info"]["players"]:
                    for player in data["info"]["players"][team]:
                        players.add(player)

for i, name in enumerate(players):
    cursor.execute(
        "INSERT OR IGNORE INTO players (player_id, full_name) VALUES (?,?)",
        (i+1, name)
    )

conn.commit()
conn.close()

print("Players imported:", len(players))
