import json
import os
import sqlite3

data_folder = "cricsheet_data"

conn = sqlite3.connect("cricbuzz.db")
cursor = conn.cursor()

match_counter = 0
ball_counter = 0

for file in os.listdir(data_folder):

    if file.endswith(".json"):

        match_counter += 1
        match_id = match_counter

        path = os.path.join(data_folder, file)

        with open(path) as f:
            data = json.load(f)

        if "innings" not in data:
            continue

        for inning in data["innings"]:

            overs = inning.get("overs", [])

            for over in overs:

                deliveries = over.get("deliveries", [])

                for ball in deliveries:

                    ball_counter += 1

                    batter = ball.get("batter")
                    bowler = ball.get("bowler")
                    runs = ball.get("runs", {}).get("batter", 0)

                    # ---------- BATSMAN ----------
                    if batter:

                        cursor.execute(
                            "SELECT player_id FROM players WHERE full_name=?",
                            (batter,)
                        )

                        result = cursor.fetchone()

                        if result:
                            player_id = result[0]

                        else:
                            cursor.execute(
                                "INSERT INTO players (full_name) VALUES (?)",
                                (batter,)
                            )
                            player_id = cursor.lastrowid

                        cursor.execute(
                            "INSERT INTO batting_stats (player_id, match_id, runs) VALUES (?,?,?)",
                            (player_id, match_id, runs)
                        )

                    # ---------- BOWLER ----------
                    if "wickets" in ball and bowler:

                        cursor.execute(
                            "SELECT player_id FROM players WHERE full_name=?",
                            (bowler,)
                        )

                        result = cursor.fetchone()

                        if result:
                            player_id = result[0]

                        else:
                            cursor.execute(
                                "INSERT INTO players (full_name) VALUES (?)",
                                (bowler,)
                            )
                            player_id = cursor.lastrowid

                        cursor.execute(
                            "INSERT INTO bowling_stats (player_id, match_id, wickets) VALUES (?,?,1)",
                            (player_id, match_id)
                        )

conn.commit()
conn.close()

print("Matches processed:", match_counter)
print("Balls processed:", ball_counter)
