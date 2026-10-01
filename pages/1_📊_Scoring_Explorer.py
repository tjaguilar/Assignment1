import streamlit as st
import pandas as pd
from data_utils import load_data
# Loads the historical scoring dataset

# Sets the title and introductory text for the page
st.title("📊 Scoring Explorer")
st.write("Filter multiple dimensions at once, then use the table and charts to compare performances.")

df = load_data()

# Session state: the selected player carries to the Player Spotlight page.
if "selected_player" not in st.session_state:
    st.session_state.selected_player = df.iloc[0]["Player"]

# Sidebar filters for players, points, years, and sort order
with st.sidebar:
    st.header("Filters")

    # Player filter
    players = sorted(df["Player"].unique())
    selected_players = st.multiselect(
        "Players",
        players,
        default=[],
        help="Leave empty to include every player.",
    )
    # Points filter
    min_points = st.slider(
        "Minimum points",
        min_value=int(df["Points"].min()),
        max_value=int(df["Points"].max()),
        value=60,
        step=1,
    )
    # Year range filter
    years = st.slider(
        "Year range",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(int(df["Year"].min()), int(df["Year"].max())),
        step=1,
    )
    # Sort order filter
    sort_order = st.radio(
        "Sort by",
        ["Points (high → low)", "Date (new → old)"],
    )

# Applies the filters to the dataset
filtered = df[df["Points"].ge(min_points) & df["Year"].between(years[0], years[1])].copy()

# Further filter by selected players if any
if selected_players:
    filtered = filtered[filtered["Player"].isin(selected_players)]

# Sort the filtered dataset based on the selected sort order
if sort_order.startswith("Points"):
    filtered = filtered.sort_values(["Points", "Date"], ascending=[False, False])
else:
    filtered = filtered.sort_values("Date", ascending=False)

# Warn the user if no games match the filters
if filtered.empty:
    st.warning("No games match those filters. Try lowering the minimum points or widening the year range.")
    st.stop()

# Derived metrics for the filtered dataset
overall_mean = df["Points"].mean()
filtered_mean = filtered["Points"].mean()
above_mean_pct = (filtered["Points"] > overall_mean).mean() * 100

# Displays key metrics for the filtered dataset
m1, m2, m3 = st.columns(3)
m1.metric("Matching games", len(filtered))
m2.metric("Highest score", f'{filtered["Points"].max()} pts')
m3.metric("Above overall average", f"{above_mean_pct:.0f}%")

# Displays the grouped scoring trend by decade
st.subheader("Grouped scoring trend")
by_decade = (
    filtered.groupby("Decade", as_index=False)
    .agg(Games=("Points", "size"), Average_Points=("Points", "mean"))
    .sort_values("Decade")
)
st.bar_chart(by_decade.set_index("Decade")["Average_Points"], y_label="Average points")

# Displays the records table and player totals in separate tabs
tab1, tab2 = st.tabs(["Records table", "Player totals"])
# Tab 1: Records table, Tab 2: Player totals
with tab1:
    display_cols = ["Rank", "Player", "Points", "Date", "Team", "Opponent"]
    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

with tab2:
    player_counts = (
        filtered.groupby("Player", as_index=False)
        .agg(Games=("Points", "size"), Best_Game=("Points", "max"), Average=("Points", "mean"))
        .sort_values(["Best_Game", "Games"], ascending=[False, False])
    )
    st.dataframe(player_counts, use_container_width=True, hide_index=True)
# Player selection for the Player Spotlight page
st.subheader("Choose a player for Player Spotlight")
chosen = st.selectbox(
    "Player",
    sorted(filtered["Player"].unique()),
    index=0,
)
# Stores the selected player in the session state and provides feedback to the user
st.session_state.selected_player = chosen
st.success(f"Selected player: {chosen}. Open **Player Spotlight** to continue your investigation.")
