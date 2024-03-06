from fastapi import FastAPI
from research_topics_ranker.fetch_data import search_pubmed

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def root():
    return {
        'Greeting':"Welcome to this amazing app"
        }


@app.get("/search_pubmed")
def search(query):
    results = search_pubmed(query)
    return f"There is {len(results)} articles published on your query ({query})"
