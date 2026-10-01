# 🏀 NBA Scoring Vault — Streamlit Ship It Project

## Problem statement

Basketball fans and students often encounter single-game scoring records as isolated facts, but it is difficult to compare performances across eras, players, teams, and time periods in one place. NBA Scoring Vault turns a historical high-scoring-game dataset into an interactive explorer so users can filter records, identify patterns, and investigate individual players.

### Information architecture

- **Home:** establishes the problem, audience, scope, and design rationale.
- **Scoring Explorer:** supports comparison and exploration through filters, metrics, grouped charts, and tables.
- **Player Spotlight:** supports a focused investigation of one player and adds a related-reading API feature.

This split follows the problem: first understand the dataset and purpose, then compare records, then investigate a specific player.

## Requirements checklist

- [x] Written problem statement visible in app
- [x] `st.columns`, `st.expander`, `st.tabs`, and `st.sidebar`
- [x] 3+ meaningful widgets (`multiselect`, `slider`, `radio`, `selectbox`)
- [x] Multiple filters applied together
- [x] `st.session_state` carries selected player from Explorer to Spotlight
- [x] Aggregated/grouped chart by decade
- [x] Derived summary metrics
- [x] Filtering and sorting
- [x] 3 pages using `pages/`
- [x] `st.cache_data` for CSV load and API request
- [x] Empty-result handling
- [x] No-auth Open Library API GET request
- [x] Accessibility-focused layout and readable labels
- [ ] Streamlit Community Cloud deployment — follow the steps below

## Data

The project includes `nba_highest_single_game_points_all_time.csv` with 101 NBA regular-season high-scoring performances.

NBA.com currently confirms the top of the scoring list, including Wilt Chamberlain's 100, Bam Adebayo's 83, Kobe Bryant's 81, and Wilt Chamberlain's 78. It also confirms Luka Dončić's 60-point game on March 19, 2026.

## API choice

The Open Library Search API was selected because it is:
1. free and requires no authentication,
2. simple to call with `requests.get()`,
3. useful for a player-focused research workflow.

The Player Spotlight page sends a query containing the selected player's name and "basketball." The response is converted into a small DataFrame and cached for one hour.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload all project files, preserving the `pages/` folder.
3. Go to Streamlit Community Cloud and create a new app.
4. Select the GitHub repository and `app.py` as the main file.
5. Deploy.
6. Copy the resulting `streamlit.app` URL into your submission.

## Oral Design Review talking points

**Problem:** Historical scoring records are hard to compare when they are scattered across lists and articles.

**Audience:** Basketball fans and students who want quick comparisons and historical context.

**Why the three pages:** Home explains the problem, Explorer helps users compare records, and Spotlight lets them investigate one player.

**Widgets:** Players, minimum points, year range, and sorting change the dataset and charts rather than acting as decoration.

**Session state:** The player selected in Scoring Explorer is carried into Player Spotlight.

**API:** Open Library adds current external reading suggestions related to the selected player without requiring an API key.

**Accessibility:** The app uses readable labels, strong default contrast, concise headings, tables alongside charts, and text descriptions rather than relying on color alone.
