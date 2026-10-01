import streamlit as st
from data_utils import load_data, search_open_library
# Loads the historical scoring dataset and defines the player selection logic
st.title("⭐ Player Spotlight")
df = load_data()
# Determines the default player for the selectbox based on the session state
players = sorted(df["Player"].unique())
default_player = st.session_state.get("selected_player", players[0])
if default_player not in players:
    default_player = players[0]
# Displays the selectbox for choosing a player
player = st.selectbox(
    "Choose a player",
    players,
    index=players.index(default_player),
)
# Stores the selected player in the session state
st.session_state.selected_player = player
# Filters the dataset for the selected player and sorts by points
player_df = df[df["Player"] == player].sort_values("Points", ascending=False).copy()
# Warn the user if the selected player has no records in the dataset
if player_df.empty:
    st.warning("There are no records for that player in the dataset.")
    st.stop()
# Computes key metrics for the selected player
best = int(player_df["Points"].max())
average = player_df["Points"].mean()
games = len(player_df)
overall_rank = int(player_df.sort_values("Points", ascending=False).iloc[0]["Rank"])
# Displays the key metrics in a four-column layout
a, b, c, d = st.columns(4)
a.metric("Best game", f"{best} points")
b.metric("Records in dataset", games)
c.metric("Player average", f"{average:.1f}")
d.metric("Best-game rank", f"#{overall_rank}")
# Displays the scoring history for the selected player
st.subheader("Scoring history")
st.line_chart(
    player_df.sort_values("Date").set_index("Date")["Points"],
    y_label="Points",
)

# Displays the highest performances for the selected player
st.subheader("Highest performances")
st.dataframe(
    player_df[["Points", "Date", "Team", "Opponent"]].head(10),
    use_container_width=True,
    hide_index=True,
)
# Displays related basketball reading using the Open Library Search API
st.subheader("Related basketball reading")
st.write(
    "This section uses the Open Library Search API as a lightweight external data feature. "
    "The request is cached for one hour and requires no API key."
)
# Attempts to fetch related basketball books from the Open Library Search API
try:
    books = search_open_library(player)
    if books.empty:
        st.info("The API returned no matching books. Try another player.")
    else:
        for _, row in books.iterrows():
            title = row["Title"]
            author = row["Author"]
            year = row["First published"]
            key = row["Open Library key"]
            if key:
                st.markdown(f"**{title}** — {author} ({year})  \nhttps://openlibrary.org{key}")
            else:
                st.markdown(f"**{title}** — {author} ({year})")
except Exception as exc:
    st.error("The reading lookup is temporarily unavailable. The historical dataset still works.")
    with st.expander("Technical details"):
        st.code(str(exc))
