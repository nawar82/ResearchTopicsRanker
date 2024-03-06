import time
import requests
import pandas as pd
from lxml import etree
from datetime import datetime

from research_topics_ranker.params import *

api_key = EUTILS_API_KEY        # It's recommended to include your NCBI API key
email = EMAIL
query = QUERY
nr_of_requests = NR_OF_REQUESTS

def search_pubmed(query):
    """search PuMed database by interacting with esearch

    Args:
        query (str): A string of the search terms

    Returns:
        data (list): A list with all PMIDs of query search results
    """
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

def get_all_text(element):
    '''Recursively get all text within an XML element, including nested tags.
    '''
    text = []
    if element.text:
        text.append(element.text)
    for child in element:
        text.append(get_all_text(child))
        if child.tail:
            text.append(child.tail)
    return ''.join(text)

def fetch_abstracts(id_list):
    """takes a list of pmid and returs their corresponding abstracts

    Args:
        id_list (list of PMIDs): Could be the output of the search_pubmed(query) function

    Returns:
        list of dictionaries: [{'PMID' : PMID, 'Abstract' : abstract}]
    """
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
        root = etree.fromstring(response.content) # type: ignore
        articles = root.xpath('//PubmedArticle')
        for article in articles:
            pmid = article.find('.//PMID').text
            abstract_text_element = article.find('.//Abstract/AbstractText')
            language = article.find('.//Language').text
            # Ensure abstract_text_element is not None before accessing its text attribute
            if abstract_text_element is not None and language == 'eng':
                abstract_text = get_all_text(abstract_text_element)
                # Further ensure the text is not None and not just whitespace
                if abstract_text and abstract_text.strip():
                    abstracts.append({"PMID": pmid, "Abstract": abstract_text})
    else:
        print("Error occurred while fetching details")
    return abstracts

def fetch_all_abstracts(id_list, nr_of_requests):
    all_abstracts = []  # Initialize an empty list to collect abstracts from all batches
    for i in range(0, len(id_list), nr_of_requests):
        batch_ids = id_list[i:i+nr_of_requests]
        abstracts = fetch_abstracts(batch_ids)
        all_abstracts.extend(abstracts)
        # Ensure not to exceed 10 requests per second
        time.sleep(0.1)
    return all_abstracts



if __name__ == "__main__":
    id_list = search_pubmed(query)
    all_abstracts = fetch_all_abstracts(id_list, nr_of_requests)

    # Convert the list of abstracts into a pandas DataFrame
    data = pd.DataFrame(all_abstracts)

    # Generate a unique filename based on the current timestamp and the first three words of the query
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    first_three_words = '-'.join(query.split()[:3]) # type: ignore
    filename = f"raw_data/abstracts_{first_three_words}_{timestamp}.csv"

    # Save the DataFrame to a CSV file
    data.to_csv(filename, index=False)

    print(f"Saved {len(all_abstracts)} abstracts to {filename}")
