import streamlit as st
import pandas as pd

st.title("🏆 ICC Men's Team Rankings")

data = {
    "Rank":[
        1,2,3,4,5,6,7,8,9,10,11,
        1,2,3,4,5,6,7,8,9,10,11,
        1,2,3,4,5,6,7,8,9,10,11
    ],

    "Team":[
        # TEST
        "Australia","South Africa","England","India","New Zealand",
        "Sri Lanka","Pakistan","West Indies","Bangladesh","Ireland","Zimbabwe",

        # ODI
        "India","New Zealand","Australia","Pakistan","South Africa",
        "Sri Lanka","Afghanistan","England","West Indies","Bangladesh","Zimbabwe",

        # T20
        "India","England","Australia","New Zealand","South Africa",
        "Pakistan","West Indies","Sri Lanka","Bangladesh","Afghanistan","Zimbabwe"
    ],

    "Matches":[
        # TEST
        36,31,46,39,29,27,25,33,30,8,18,

        # ODI
        45,47,38,41,41,47,28,43,41,38,24,

        # T20
        83,55,49,64,63,84,74,60,67,52,72
    ],

    "Rating":[
        # TEST
        128,116,109,104,98,88,82,69,63,23,12,

        # ODI
        119,114,109,105,98,98,95,88,77,76,54,

        # T20
        272,260,258,250,245,238,235,227,223,221,202
    ],

    "Points":[
        # TEST
        4604,3581,5013,4064,2839,2364,2050,2270,1888,185,208,

        # ODI
        5377,5370,4134,4294,4022,4600,2657,3782,3173,2882,1291,

        # T20
        22613,14300,12645,16002,15432,20002,17424,13593,14925,11504,14539
    ],

    "Format":[
        "TEST","TEST","TEST","TEST","TEST","TEST","TEST","TEST","TEST","TEST","TEST",
        "ODI","ODI","ODI","ODI","ODI","ODI","ODI","ODI","ODI","ODI","ODI",
        "T20","T20","T20","T20","T20","T20","T20","T20","T20","T20","T20"
    ]
}

df = pd.DataFrame(data)

format_type = st.selectbox(
    "Select Format",
    ["TEST","ODI","T20"]
)

filtered = df[df["Format"] == format_type]

st.subheader(f"{format_type} Team Rankings")

st.dataframe(filtered)
