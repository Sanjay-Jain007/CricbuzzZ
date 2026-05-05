import requests
import sqlite3

API_KEY = "fefa6d7e-930d-4d82-8f7a-e1d94bc3e9b2"

url = f"https://api.cricapi.com/v1/players?apikey={API_KEY}&offset=0"

response = requests.get(url)
data = response.json()

conn = sqlite3.connect("cricbuzz.db")
cursor = conn.cursor()

for player in data.get("data", []):

    name = player.get("name")
    country = player.get("country")

    cursor.execute(
        "INSERT INTO players (full_name) VALUES (?)",
        (name,)
    )

conn.commit()
conn.close()

print("Players imported successfully")
