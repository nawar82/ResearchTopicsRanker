# frontend.py
import streamlit as st

# This could be your main page or just configurations that apply to the whole app
st.title("Research Topics Ranker")
st.write("Navigate to other pages using the sidebar.")

st.markdown('''
    **search and fetch** is an application that will search PubMed database for
    the terms you provide and return a database with all English abstracts.

    **all words cloud** uses tf-idf vectorizer to weigh words after preprocessing
    all abstracts and plot the top 500 words in a word cloud.

    **top unique words** is using machine learning techniques to model all
    extracted topis from the extracted abstracts and return the top words/phrases
    that have the heighest weights over all topics. We use LDE for topic modelling.

    **words per topic** is using machine learning techniques to model all
    extracted topis from the extracted abstracts and return the top words/phrases
    in each of the topics. We use LDE for topic modelling.
''')
