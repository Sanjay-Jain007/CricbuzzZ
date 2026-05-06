import streamlit as st
import requests

st.title("🏏 Match Explorer")

category = st.selectbox(
    "Select Match Category",
    ["International", "League", "Domestic", "Women"]
)

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

headers = {
    "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

# =========================
# HANDLE API RESPONSE
# =========================

if response.status_code == 200:

    data = response.json()

    found_matches = False

    for match_type in data.get("typeMatches", []):

        if match_type.get("matchType") == category:

            for series in match_type.get("seriesMatches", []):

                wrapper = series.get("seriesAdWrapper")

                if wrapper:

                    series_name = wrapper.get("seriesName", "Series")

                    st.header(series_name)

                    for match in wrapper.get("matches", []):

                        found_matches = True

                        info = match.get("matchInfo", {})
                        score = match.get("matchScore", {})

                        match_id = info.get("matchId")

                        team1 = info.get("team1", {}).get("teamName", "Team 1")
                        team2 = info.get("team2", {}).get("teamName", "Team 2")

                        team1_short = info.get("team1", {}).get("teamSName", "")
                        team2_short = info.get("team2", {}).get("teamSName", "")

                        status = info.get("status", "No status")
                        match_desc = info.get("matchDesc", "")

                        venue = info.get("venueInfo", {}).get("ground", "")
                        city = info.get("venueInfo", {}).get("city", "")

                        st.subheader(f"{team1} vs {team2}")

                        st.write(f"🏟️ {venue}, {city}")
                        st.write(f"📌 {match_desc}")

                        # =========================
                        # SCORE DISPLAY
                        # =========================

                        team1_score = "N/A"
                        team2_score = "N/A"

                        if "team1Score" in score and "inngs1" in score["team1Score"]:
                            inngs = score["team1Score"]["inngs1"]

                            runs = inngs.get("runs", 0)
                            wkts = inngs.get("wickets", 0)
                            overs = inngs.get("overs", 0)

                            team1_score = f"{runs}/{wkts} ({overs})"

                        if "team2Score" in score and "inngs1" in score["team2Score"]:
                            inngs = score["team2Score"]["inngs1"]

                            runs = inngs.get("runs", 0)
                            wkts = inngs.get("wickets", 0)
                            overs = inngs.get("overs", 0)

                            team2_score = f"{runs}/{wkts} ({overs})"

                        st.write(f"### {team1_short}: {team1_score}")
                        st.write(f"### {team2_short}: {team2_score}")

                        st.success(status)

                        # =========================
                        # SCORECARD BUTTON
                        # =========================

                        if st.button(f"View Scorecard {match_id}"):

                            score_url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"

                            score_response = requests.get(score_url, headers=headers)

                            if score_response.status_code == 200:

                                score_data = score_response.json()

                                st.subheader("📋 Scorecard")

                                if "scoreCard" in score_data:

                                    for inning in score_data["scoreCard"]:

                                        team = inning["batTeamDetails"]["batTeamName"]

                                        st.write(f"## {team}")

                                        batsmen = inning["batTeamDetails"]["batsmenData"]

                                        for player in batsmen.values():

                                            name = player.get("batName", "")
                                            runs = player.get("runs", 0)
                                            balls = player.get("balls", 0)
                                            fours = player.get("fours", 0)
                                            sixes = player.get("sixes", 0)

                                            st.write(
                                                f"🏏 {name} — {runs} ({balls}) | 4s: {fours} | 6s: {sixes}"
                                            )

                                else:
                                    st.warning("Scorecard not available")

                            else:
                                st.error("Could not fetch scorecard")

                        st.markdown("---")

    if not found_matches:
        st.warning("No matches found for selected category.")

elif response.status_code == 204:
    st.warning("No recent matches available right now.")

else:
    st.error(f"API Error: {response.status_code}")
    st.write(response.text)
