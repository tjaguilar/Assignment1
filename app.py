import streamlit as st

st.set_page_config(
    page_title="NBA Scoring Vault",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏀 NBA Scoring Vault")
st.caption("Explore the highest individual scoring games in NBA regular-season history.")

with st.sidebar:
    st.header("Navigation")
    st.write("Use the pages above to explore records and player profiles.")
    st.divider()
    st.markdown("**Dataset:** 101 high-scoring NBA games")
    st.markdown("**Scope:** regular-season single-game scoring")
    st.markdown("**API:** Open Library, no authentication required")

st.subheader("The problem")
st.write(
    "Basketball fans and students often encounter single-game scoring records as isolated "
    "facts, but it is difficult to compare those performances across eras, players, teams, "
    "and time periods in one place. This app turns a verified historical scoring dataset into "
    "an interactive explorer so users can filter the records, see patterns, and investigate "
    "individual players without digging through separate lists."
)

st.subheader("Who is this for?")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Audience", "Fans & students")
with c2:
    st.metric("Records", "101 games")
with c3:
    st.metric("Interactive pages", "3")

st.subheader("Why this page structure?")
st.markdown(
    """
- **Home:** explains the problem, scope, and how the app is organized.
- **Scoring Explorer:** answers comparison questions using filters, sorting, and charts.
- **Player Spotlight:** focuses on one player and adds related reading through a live API.
"""
)

with st.expander("Data and source notes"):
    st.write(
        "The included CSV contains 101 high-scoring NBA regular-season performances. "
        "The app treats the CSV as the main historical dataset. The Player Spotlight page "
        "also makes a cached, no-authentication GET request to the Open Library Search API "
        "to find basketball-related reading connected to the selected player."
    )
    st.info(
        "Accessibility choices: high-contrast default Streamlit components, descriptive "
        "headings, short labels, readable tables, and information conveyed with text as "
        "well as charts."
    )
