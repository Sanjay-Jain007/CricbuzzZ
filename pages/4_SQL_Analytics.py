import streamlit as st
import sqlite3
import pandas as pd

st.title("📊 Cricket SQL Analytics Dashboard")

conn = sqlite3.connect("cricbuzz.db")

menu = st.selectbox(
    "Select Query",
    [
        "1 Top Run Scorers",
        "2 Best Batting Average",
        "3 Most Matches Played",
        "4 Most Wickets",
        "5 Best Bowling Performance",
        "6 Best All Rounders",
        "7 Runs Distribution",
        "8 Wickets Distribution",

        "9 Players With 10000+ Runs",
        "10 Players With 500+ Wickets",
        "11 Players With 100+ Matches",
        "12 Players With 5000+ Runs",
        "13 Players With 100+ Wickets",
        "14 Top 20 Batters",
        "15 Top 20 Bowlers",
        "16 Players With Both Runs and Wickets",
        "17 Players With Zero Wickets",
        "18 Players With Zero Runs",
        "19 Top Players Alphabetically",
        "20 Players With Highest Runs",
        "21 Players With Highest Wickets",
        "22 Players Starting With A",
        "23 Players Starting With S",
        "24 Players With Runs Between 5000 and 10000",
        "25 Players With Wickets Between 200 and 500"
    ]
)

# ---------- 1 ----------
if menu == "1 Top Run Scorers":

    query = """
    SELECT players.full_name,
           MAX(batting_stats.runs) AS total_runs
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    GROUP BY players.full_name
    ORDER BY total_runs DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    st.subheader("Top Run Scorers")
    st.dataframe(df)
    st.bar_chart(df.set_index("full_name"))

# ---------- 2 ----------
elif menu == "2 Best Batting Average":

    query = """
    SELECT players.full_name,
           MAX(batting_stats.runs) AS runs
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    ORDER BY runs DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    st.subheader("Best Batting Average")
    st.dataframe(df)

# ---------- 3 ----------
elif menu == "3 Most Matches Played":

    query = """
    SELECT players.full_name,
           COUNT(batting_stats.match_id) AS matches
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    GROUP BY players.full_name
    ORDER BY matches DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    st.subheader("Most Matches Played")
    st.dataframe(df)

# ---------- 4 ----------
elif menu == "4 Most Wickets":

    query = """
    SELECT players.full_name,
           MAX(bowling_stats.wickets) AS wickets
    FROM players
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    GROUP BY players.full_name
    ORDER BY wickets DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    st.subheader("Most Wickets")
    st.dataframe(df)
    st.bar_chart(df.set_index("full_name"))

# ---------- 5 ----------
elif menu == "5 Best Bowling Performance":

    query = """
    SELECT players.full_name,
           MAX(bowling_stats.wickets) AS best_figures
    FROM players
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    GROUP BY players.full_name
    ORDER BY best_figures DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    st.subheader("Best Bowling Performance")
    st.dataframe(df)

# ---------- 6 ----------
elif menu == "6 Best All Rounders":

    query = """
    SELECT players.full_name,
           MAX(batting_stats.runs) AS runs,
           MAX(bowling_stats.wickets) AS wickets
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    ORDER BY runs DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)

    st.subheader("Best All Rounders")
    st.dataframe(df)

# ---------- 7 ----------
elif menu == "7 Runs Distribution":

    query = """
    SELECT full_name,
           MAX(runs) AS runs
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    GROUP BY full_name
    ORDER BY runs DESC
    LIMIT 20
    """

    df = pd.read_sql_query(query, conn)

    st.bar_chart(df.set_index("full_name"))

# ---------- 8 ----------
elif menu == "8 Wickets Distribution":

    query = """
    SELECT full_name,
           MAX(wickets) AS wickets
    FROM players
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    GROUP BY full_name
    ORDER BY wickets DESC
    LIMIT 20
    """

    df = pd.read_sql_query(query, conn)

    st.bar_chart(df.set_index("full_name"))

# ---------- SIMPLE QUERIES ----------
elif menu == "9 Players With 10000+ Runs":

    df = pd.read_sql_query("""
    SELECT full_name,runs
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    WHERE runs >= 10000
    """, conn)

    st.dataframe(df)

elif menu == "10 Players With 500+ Wickets":

    df = pd.read_sql_query("""
    SELECT full_name,wickets
    FROM players
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    WHERE wickets >= 500
    """, conn)

    st.dataframe(df)

elif menu == "11 Players With 100+ Matches":

    df = pd.read_sql_query("""
    SELECT full_name
    FROM players
    LIMIT 100
    """, conn)

    st.dataframe(df)

elif menu == "12 Players With 5000+ Runs":

    df = pd.read_sql_query("""
    SELECT full_name,runs
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    WHERE runs >= 5000
    """, conn)

    st.dataframe(df)

elif menu == "13 Players With 100+ Wickets":

    df = pd.read_sql_query("""
    SELECT full_name,wickets
    FROM players
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    WHERE wickets >= 100
    """, conn)

    st.dataframe(df)

elif menu == "14 Top 20 Batters":

    df = pd.read_sql_query("""
    SELECT full_name,runs
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    ORDER BY runs DESC
    LIMIT 20
    """, conn)

    st.dataframe(df)

elif menu == "15 Top 20 Bowlers":

    df = pd.read_sql_query("""
    SELECT full_name,wickets
    FROM players
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    ORDER BY wickets DESC
    LIMIT 20
    """, conn)

    st.dataframe(df)

elif menu == "16 Players With Both Runs and Wickets":

    df = pd.read_sql_query("""
    SELECT players.full_name,runs,wickets
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    """, conn)

    st.dataframe(df)

elif menu == "17 Players With Zero Wickets":

    df = pd.read_sql_query("""
    SELECT full_name
    FROM players
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    WHERE wickets = 0
    """, conn)

    st.dataframe(df)

elif menu == "18 Players With Zero Runs":

    df = pd.read_sql_query("""
    SELECT full_name
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    WHERE runs = 0
    """, conn)

    st.dataframe(df)

elif menu == "19 Top Players Alphabetically":

    df = pd.read_sql_query("""
    SELECT full_name
    FROM players
    ORDER BY full_name
    LIMIT 50
    """, conn)

    st.dataframe(df)

elif menu == "20 Players With Highest Runs":

    df = pd.read_sql_query("""
    SELECT full_name,runs
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    ORDER BY runs DESC
    LIMIT 5
    """, conn)

    st.dataframe(df)

elif menu == "21 Players With Highest Wickets":

    df = pd.read_sql_query("""
    SELECT full_name,wickets
    FROM players
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    ORDER BY wickets DESC
    LIMIT 5
    """, conn)

    st.dataframe(df)

elif menu == "22 Players Starting With A":

    df = pd.read_sql_query("""
    SELECT full_name
    FROM players
    WHERE full_name LIKE 'A%'
    """, conn)

    st.dataframe(df)

elif menu == "23 Players Starting With S":

    df = pd.read_sql_query("""
    SELECT full_name
    FROM players
    WHERE full_name LIKE 'S%'
    """, conn)

    st.dataframe(df)

elif menu == "24 Players With Runs Between 5000 and 10000":

    df = pd.read_sql_query("""
    SELECT full_name,runs
    FROM players
    JOIN batting_stats
    ON players.player_id = batting_stats.player_id
    WHERE runs BETWEEN 5000 AND 10000
    """, conn)

    st.dataframe(df)

elif menu == "25 Players With Wickets Between 200 and 500":

    df = pd.read_sql_query("""
    SELECT full_name,wickets
    FROM players
    JOIN bowling_stats
    ON players.player_id = bowling_stats.player_id
    WHERE wickets BETWEEN 200 AND 500
    """, conn)

    st.dataframe(df)

conn.close()
