import streamlit as st
import feedparser
import re

st.title("📰 Latest Cricket News")

st.write("Stay updated with the latest cricket news.")

rss_url = "https://news.google.com/rss/search?q=cricket"

feed = feedparser.parse(rss_url)

for entry in feed.entries[:10]:

    st.subheader(entry.title)

    st.write(entry.published)

    # Remove HTML tags
    clean_summary = re.sub("<.*?>", "", entry.summary)

    st.write(clean_summary)

    st.markdown(f"[Read Full Article]({entry.link})")

    st.markdown("---")
