import streamlit as st
import matplotlib.pyplot as plt
import requests
import nltk
import nltk.data
nltk.download('punkt', download_dir="/home/appuser/nltk_data")
nltk.download('stopwords', download_dir="/home/appuser/nltk_data")
nltk.download('wordnet', download_dir="/home/appuser/nltk_data")

from research_topics_ranker.fetch_data import *
from research_topics_ranker.vectorize import *
from research_topics_ranker.main import *
from api.fast import plot_words_per_topics

st.set_option('deprecation.showPyplotGlobalUse', False)

# Title for your app
st.title('Research Topics Ranker')
st.header('Search PubMed')


with st.form(key='params_for_api'):

    query = st.text_input('searched terms in pubmed', value="")

    submitted = st.form_submit_button('Top words per topics')
    if submitted:
        st.pyplot(plot_words_per_topics(query))



url = "https://research-topics-ranker-gs34zyaenq-ew.a.run.app/plot_words_per_topics"
#url = "http://127.0.0.1:8000/plot_words_per_topics"
params = {
    "query" : ""
}

response = requests.get(url, params)
