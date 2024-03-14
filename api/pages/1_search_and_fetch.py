import streamlit as st
import requests

from research_topics_ranker.fetch_data import *
from research_topics_ranker.vectorize import *


# Title for your app
st.title('Research Topics Ranker')
st.header('Search PubMed')

query = st.text_area('Search PubMed') # type: ignore

@st.cache  # This decorator caches the results
def search_pubmed_cached(query):
    return search_pubmed(query)

@st.cache  # This decorator caches the results
def fetch_all_abstracts_cached(results, nr_of_requests):
    return fetch_all_abstracts(results, nr_of_requests)


#Creating a search bar
if query:  # Checks if the query is not empty
    # Call the search function only if there is a query
    results = search_pubmed_cached(query)
    # Display the number of articles
    st.write(f"There are {len(results)} articles published on your query ({query})")

    df = pd.DataFrame(fetch_all_abstracts_cached(results, nr_of_requests))
    # this slider allows the user to select a number of lines
    # to display in the dataframe
    # the selected value is returned by st.slider
    line_count = st.slider('Select a line count', 1, len(df), 1)
    # and used to select the displayed lines
    head_df = df.head(line_count)
    st.write(head_df)

else:
    # Message displayed before the user inputs a query
    st.write("Please enter a query to search PubMed articles.")







url = "http://127.0.0.1:8000/search_pubmed"
params = {
    "query" : ""
}

response = requests.get(url, params)
