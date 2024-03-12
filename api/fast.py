from fastapi import FastAPI
from research_topics_ranker.fetch_data import search_pubmed
import pickle
import pandas as pd

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



@app.get("/analysis")
def analysis(data):

    # Load the fitted pipeline from the pickle file
    with open('models/lda_model.pkl', 'rb') as file:
        model = pickle.load(file)

    document_topic_mixture = pd.DataFrame(model.fit_transform(data['Abstract']),
                                      columns = [f"topic_{i}" for i in range(1, 11)],
                                      index = data['PMID'])

    return document_topic_mixture
#data = pd.DataFrame({'PMID': [123456], 'Abstract': ['This is the first abstract']})
