from pathlib import Path #import Path for handling file paths
import requests #import requests for making HTTP requests
import pandas as pd #import pandas for data manipulation
import streamlit as st #import streamlit for building the web app

DATA_PATH = Path(__file__).resolve().parent / "nba_highest_single_game_points_all_time.csv" #define the path to the CSV file containing the historical scoring data

@st.cache_data #caches the result of the load_data function to improve performance
def load_data(): #loads the historical scoring dataset from the CSV file
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"]) #reads the CSV file into a pandas DataFrame and parses the "Date" column as datetime
    df["Year"] = df["Date"].dt.year #extracts the year from the "Date" column
    df["Decade"] = (df["Year"] // 10) * 10 #calculates the decade for each record
    df["Points Above 50"] = df["Points"] - 50 #calculates the points scored above 50 for each record
    return df #returns the processed DataFrame

@st.cache_data(ttl=3600, show_spinner=False) #caches the result of the search_open_library function for one hour to improve performance
def search_open_library(player_name): #searches for basketball books related to the given player using the Open Library Search API
    """Cached, no-auth GET request used by the Player Spotlight page.""" #docstring explaining the purpose of the function
    query = f'"{player_name}" basketball' #constructs the search query for the Open Library API
    url = "https://openlibrary.org/search.json" #defines the URL for the Open Library Search API
    response = requests.get( #makes a GET request to the Open Library Search API with the specified query and parameters
        url, #the URL for the Open Library Search API
        params={"q": query, "limit": 8, "fields": "title,author_name,first_publish_year,key"}, #query parameters for the API request
        timeout=10, #sets a timeout of 10 seconds for the request
    )
    response.raise_for_status() #raises an exception if the HTTP request returned an unsuccessful status code
    payload = response.json() #parses the JSON response from the API into a Python dictionary
    docs = payload.get("docs", []) #extracts the list of book documents from the API response
    rows = [] #initializes an empty list to store the processed book data
    for doc in docs: #iterates over each book document in the API response
        title = doc.get("title") #extracts the title of the book from the document
        if not title: #skips the document if the title is missing
            continue #skip this document and move to the next one if the title is missing
        rows.append( #adds the processed book data to the list of rows
            {
                "Title": title, #the title of the book
                "Author": ", ".join(doc.get("author_name", [])[:2]) or "Unknown", #the author(s) of the book, limited to the first two authors
                "First published": doc.get("first_publish_year", "—"), #the year the book was first published
                "Open Library key": doc.get("key", ""), #the unique key for the book in the Open Library database
            }
        )
    return pd.DataFrame(rows) #converts the list of processed book data into a pandas DataFrame and returns it
