import pandas as pd
from fastapi import FastAPI
import wordcloud
from research_topics_ranker.fetch_data import *
from research_topics_ranker.vectorize import *
from research_topics_ranker.main import *

from sklearn.feature_extraction.text import TfidfVectorizer

from research_topics_ranker.params import *


app = FastAPI()

@app.get("/")
def root():
    return {
        'Greeting':"Welcome to this amazing app"
        }

@app.get("/search_pubmed")
def search(query):
    results = search_pubmed(query)
    return f"There is {len(results)} articles published on your query ({query})"

@app.get("/AllWordsCloud")
def AllWordsCloud(query):

    id_list = search_pubmed(query)
    all_abstracts = fetch_all_abstracts(id_list, nr_of_requests)

    # Convert the list of abstracts into a pandas DataFrame
    data = pd.DataFrame(all_abstracts)
    data['clean_text'] = data['Abstract'].apply(preprocessing)

    # Vectorizing the data
    vectorizer = TfidfVectorizer(ngram_range=(2, 3),
                                max_df=0.6).fit(data['clean_text'])

    vectorized_documents = pd.DataFrame(vectorizer.transform(data['clean_text']).toarray(),
                                        columns=vectorizer.get_feature_names_out())
    sum_tfidf = vectorized_documents.sum(axis=0)

    tfidf_list = [(word, sum_tfidf[word]) for word, idx in vectorizer.vocabulary_.items()]

    sorted_tfidf_list = sorted(tfidf_list, key=lambda x: x[1], reverse=True)

    # Convert the sorted TF-IDF list to a dictionary
    tfidf_dict = {word: score for word, score in sorted_tfidf_list}
    wordcloudimg = gen_wordcloud(tfidf_dict)

    return wordcloudimg

@app.get("/top_unique_words")
def top_unique_words(query):
    id_list = search_pubmed(query)
    all_abstracts = fetch_all_abstracts(id_list, nr_of_requests)

    # Convert the list of abstracts into a pandas DataFrame
    data = pd.DataFrame(all_abstracts)
    data['clean_text'] = data['Abstract'].apply(preprocessing)

    # Vectorizing the data
    vectorizer = TfidfVectorizer(ngram_range=(2, 3),
                                max_df=0.6).fit(data['clean_text'])

    vectorized_documents = pd.DataFrame(vectorizer.transform(data['clean_text']).toarray(),
                                        columns=vectorizer.get_feature_names_out())

    lda_model = lda_model_fit(n_components=n_components,
                            max_iter = max_iter,
                            vectorized_documents = vectorized_documents)

    topics = topics_list(lda_model, vectorizer, n_components)

    return plot_top_unique_words(topics)

@app.get("/plot_words_per_topics")
def plot_words_per_topics(query):
    id_list = search_pubmed(query)
    all_abstracts = fetch_all_abstracts(id_list, nr_of_requests)

    # Convert the list of abstracts into a pandas DataFrame
    data = pd.DataFrame(all_abstracts)
    data['clean_text'] = data['Abstract'].apply(preprocessing)

    # Vectorizing the data
    vectorizer = TfidfVectorizer(ngram_range=(2, 3),
                                max_df=0.6).fit(data['clean_text'])

    vectorized_documents = pd.DataFrame(vectorizer.transform(data['clean_text']).toarray(),
                                        columns=vectorizer.get_feature_names_out())

    lda_model = lda_model_fit(n_components=n_components,
                            max_iter = max_iter,
                            vectorized_documents = vectorized_documents)

    topics = topics_list(lda_model, vectorizer, n_components)

    return graph_topics(topics)
