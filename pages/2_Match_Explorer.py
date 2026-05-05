import streamlit as st
import requests

st.title("🏏 Match Explorer")

category = st.selectbox(
    "Select Match Category",
    ["International", "League", "Domestic", "Women"]
)

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

headers = {
    "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:

    data = response.json()

    for match_type in data.get("typeMatches", []):

        if match_type["matchType"] == category:

            for series in match_type.get("seriesMatches", []):

                wrapper = series.get("seriesAdWrapper")

                if wrapper:

                    for match in wrapper.get("matches", []):

                        info = match.get("matchInfo", {})
                        score = match.get("matchScore", {})

                        match_id = info.get("matchId")

                        team1 = info.get("team1", {}).get("teamName")
                        team2 = info.get("team2", {}).get("teamName")

                        status = info.get("status")

                        st.subheader(f"{team1} vs {team2}")

                        # show score
                        team1_score = ""
                        team2_score = ""

                        if "team1Score" in score:
                            runs = score["team1Score"]["inngs1"].get("runs", "")
                            wkts = score["team1Score"]["inngs1"].get("wickets", "")
                            team1_score = f"{runs}/{wkts}"

                        if "team2Score" in score:
                            runs = score["team2Score"]["inngs1"].get("runs", "")
                            wkts = score["team2Score"]["inngs1"].get("wickets", "")
                            team2_score = f"{runs}/{wkts}"

                        st.write(f"Score: {team1} {team1_score} | {team2} {team2_score}")

                        st.success(status)

                        # BUTTON
                        if st.button(f"View Scorecard {match_id}"):
                            score_url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"


                            score_response = requests.get(score_url, headers=headers)

                            score_data = score_response.json()

                            st.subheader("Scorecard")

                            if "scoreCard" in score_data:

                                for inning in score_data["scoreCard"]:

                                    team = inning["batTeamDetails"]["batTeamName"]

                                    st.write("###", team)

                                    for player in inning["batTeamDetails"]["batsmenData"].values():

                                        name = player["batName"]
                                        runs = player["runs"]
                                        balls = player["balls"]

                                        st.write(f"{name} — {runs} ({balls})")

                            else:
                                st.warning("Scorecard not available")

                        st.markdown("---")

else:
    st.error("Failed to fetch matches")
