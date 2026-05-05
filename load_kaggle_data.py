import pandas as pd
import sqlite3

df = pd.read_csv("players.csv")

# keep only useful columns
df = df[["Name","Mat","Runs","Wkt"]]

# remove bad rows
df = df[df["Name"].notna()]
df = df[df["Name"].str.contains("[A-Za-z]", na=False)]

# clean numbers
df["Runs"] = pd.to_numeric(df["Runs"].astype(str).str.replace(",",""), errors="coerce").fillna(0)
df["Wkt"] = pd.to_numeric(df["Wkt"].astype(str).str.replace(",",""), errors="coerce").fillna(0)
df["Mat"] = pd.to_numeric(df["Mat"], errors="coerce").fillna(0)

conn = sqlite3.connect("cricbuzz.db")
cursor = conn.cursor()

for _, row in df.iterrows():

    name = row["Name"]
    matches = int(row["Mat"])
    runs = int(row["Runs"])
    wickets = int(row["Wkt"])

    cursor.execute(
        "INSERT INTO players (full_name) VALUES (?)",
        (name,)
    )

    player_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO batting_stats (player_id, match_id, runs) VALUES (?, ?, ?)",
        (player_id, matches, runs)
    )

    cursor.execute(
        "INSERT INTO bowling_stats (player_id, match_id, wickets) VALUES (?, ?, ?)",
        (player_id, matches, wickets)
    )

conn.commit()
conn.close()

print("Dataset imported successfully")
