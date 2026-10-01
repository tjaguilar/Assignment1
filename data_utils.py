from pathlib import Path
import requests
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent / "nba_highest_single_game_points_all_time.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df["Year"] = df["Date"].dt.year
    df["Decade"] = (df["Year"] // 10) * 10
    df["Points Above 50"] = df["Points"] - 50
    return df

@st.cache_data(ttl=3600, show_spinner=False)
def search_open_library(player_name):
    """Cached, no-auth GET request used by the Player Spotlight page."""
    query = f'"{player_name}" basketball'
    url = "https://openlibrary.org/search.json"
    response = requests.get(
        url,
        params={"q": query, "limit": 8, "fields": "title,author_name,first_publish_year,key"},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    docs = payload.get("docs", [])
    rows = []
    for doc in docs:
        title = doc.get("title")
        if not title:
            continue
        rows.append(
            {
                "Title": title,
                "Author": ", ".join(doc.get("author_name", [])[:2]) or "Unknown",
                "First published": doc.get("first_publish_year", "—"),
                "Open Library key": doc.get("key", ""),
            }
        )
    return pd.DataFrame(rows)
