import requests
import pandas as pd
from lxml import etree

from research_topics_ranker.params import *

api_key = EUTILS_API_KEY        # It's recommended to include your NCBI API key
email = EMAIL
query = QUERY


def search_pubmed(query):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": "10000",
        "usehistory": "y",
        "email": email,
        "api_key": api_key,
        "retmode": "json"  # Set retmode to json
    }
    #breakpoint()
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        #breakpoint()
        data = requests.get(base_url, params=params).json()
        #id_list = data["esearchresult"]["idlist"]
        if data['esearchresult']['count'] == data['esearchresult']['retmax']:
            print(f"You have a total of {data['esearchresult']['count']} articles and getting {data['esearchresult']['retmax']} articles to fetch their abstracts")
        else:
            print(f"Please be aware that your search terms returned {data['esearchresult']['count']} articles but you are getting only {data['esearchresult']['retmax']} for fetching their abstracts")
        return data["esearchresult"]["idlist"]
    else:
        print("Error occurred while searching")
        return []


id_list = search_pubmed(query)

def fetch_abstracts(id_list):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    ids = ','.join(id_list)
    params = {
        "db": "pubmed",
        "retmode": "xml",
        "id": ids,
        "api_key": api_key
    }
    response = requests.get(base_url, params=params)
    abstracts = []
    if response.status_code == 200:
        root = etree.fromstring(response.content)
        articles = root.xpath('//PubmedArticle')
        for article in articles:
            pmid = article.find('.//PMID').text
            abstract_text = article.find('.//Abstract/AbstractText')
            if abstract_text is not None:
                abstracts.append({"PMID": pmid, "Abstract": abstract_text.text})
    else:
        print("Error occurred while fetching details")
    return abstracts


print(fetch_abstracts(id_list))
