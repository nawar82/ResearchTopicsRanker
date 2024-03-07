from fastapi import FastAPI
from research_topics_ranker.fetch_data import search_pubmed

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
