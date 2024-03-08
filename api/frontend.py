import streamlit as st
import requests

from research_topics_ranker.fetch_data import search_pubmed


# Title for your app
st.title('Research Topics Ranker')

st.header('Search PubMed')

query = st.text_area('Search PubMed') # type: ignore

#Creating a search bar
if query:  # Checks if the query is not empty
    # Call the search function only if there is a query
    results = search_pubmed(query)

    # Display the number of articles
    st.write(f"There are {len(results)} articles published on your query ({query})")
else:
    # Message displayed before the user inputs a query
    st.write("Please enter a query to search PubMed articles.")

url = "http://127.0.0.1:8000/search_pubmed"
params = {
    "query" : ""
}

response = requests.get(url, params)
