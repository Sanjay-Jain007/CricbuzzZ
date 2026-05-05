import streamlit as st
import sqlite3
import pandas as pd

st.title("🏏 Cricbuzz Analytics Dashboard")

st.markdown("Welcome to the Cricket Analytics Platform")

conn = sqlite3.connect("cricbuzz.db")

# -------------------------
# TOP RUN SCORERS
# -------------------------

st.subheader("🔥 Top Run Scorers")

query = """
SELECT players.full_name,
       MAX(batting_stats.runs) AS runs
FROM players
JOIN batting_stats
ON players.player_id = batting_stats.player_id
GROUP BY players.full_name
ORDER BY runs DESC
LIMIT 5
"""

df = pd.read_sql_query(query, conn)

st.dataframe(df)
st.bar_chart(df.set_index("full_name"))

# -------------------------
# TOP WICKET TAKERS
# -------------------------

st.subheader("🎯 Top Wicket Takers")

query2 = """
SELECT players.full_name,
       MAX(bowling_stats.wickets) AS wickets
FROM players
JOIN bowling_stats
ON players.player_id = bowling_stats.player_id
GROUP BY players.full_name
ORDER BY wickets DESC
LIMIT 5
"""

df2 = pd.read_sql_query(query2, conn)

st.dataframe(df2)
st.bar_chart(df2.set_index("full_name"))

conn.close()

st.markdown("---")

st.info("Use the sidebar to explore Live Matches, Players, and SQL Analytics.")
