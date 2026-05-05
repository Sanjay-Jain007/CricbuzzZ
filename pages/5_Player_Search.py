import streamlit as st
import sqlite3
import pandas as pd

st.title("🔎 Player Search")

player_name = st.text_input("Enter Player Name")

if player_name:

    conn = sqlite3.connect("cricbuzz.db")

    query = """
    SELECT 
        players.full_name,
        COUNT(batting_stats.match_id) AS matches,
        SUM(batting_stats.runs) AS total_runs,
        ROUND(AVG(batting_stats.runs),2) AS avg_runs,
        SUM(bowling_stats.wickets) AS total_wickets
    FROM players
    LEFT JOIN batting_stats 
        ON players.player_id = batting_stats.player_id
    LEFT JOIN bowling_stats 
        ON players.player_id = bowling_stats.player_id
    WHERE players.full_name LIKE ?
    GROUP BY players.full_name
    """

    df = pd.read_sql_query(query, conn, params=(f"%{player_name}%",))

    if df.empty:
        st.warning("Player not found in database")
    else:
        st.dataframe(df, use_container_width=True)

    conn.close()
