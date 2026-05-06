import streamlit as st
import requests

st.title("🔴 Live Cricket Matches")

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

headers = {
    "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    # show matches here

elif response.status_code == 204:
    st.warning("No live matches available right now.")

else:
    st.error(f"API Error: {response.status_code}")
    st.write(response.text)

if response.status_code == 200:

    data = response.json()

    type_matches = data.get("typeMatches", [])

    if not type_matches:
        st.info("No live matches right now")

    for match_type in type_matches:

        for series in match_type.get("seriesMatches", []):

            wrapper = series.get("seriesAdWrapper")

            if wrapper:

                for match in wrapper.get("matches", []):

                    info = match.get("matchInfo", {})
                    score = match.get("matchScore", {})

                    team1 = info.get("team1", {}).get("teamName")
                    team2 = info.get("team2", {}).get("teamName")
                    status = info.get("status")

                    st.subheader(f"{team1} vs {team2}")

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

                    st.write(f"{team1} {team1_score} | {team2} {team2_score}")
                    st.success(status)

                    st.markdown("---")


