import streamlit as st
import matplotlib.pyplot as plt
import requests
import nltk
import nltk.data
nltk.download('punkt', download_dir="/home/appuser/nltk_data")
nltk.download('stopwords', download_dir="/home/appuser/nltk_data")

from research_topics_ranker.fetch_data import *
from research_topics_ranker.vectorize import *
from research_topics_ranker.main import *
from api.fast import AllWordsCloud

nltk.data.path = ['/home/appuser/nltk_data']
st.set_option('deprecation.showPyplotGlobalUse', False)

# Title for your app
st.title('Research Topics Ranker')
st.header('Search PubMed')


with st.form(key='params_for_api'):

    query = st.text_input('searched terms in pubmed', value="")

    submitted = st.form_submit_button('Word cloud for top words over all topics')
    if submitted:
        st.pyplot(AllWordsCloud(query))


url = "https://research-topics-ranker-gs34zyaenq-ew.a.run.app/AllWordsCloud"
#url = "http://127.0.0.1:8000/AllWordsCloud"
params = {
    "query" : ""
}

response = requests.get(url, params)
