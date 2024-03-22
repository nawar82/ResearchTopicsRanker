from research_topics_ranker.fetch_data import *
import pandas as pd

query = QUERY
nr_of_requests = NR_OF_REQUESTS


def top_journals(n=10):

    id_list = search_pubmed(query)
    all_abstracts = fetch_all_abstracts(id_list, nr_of_requests)
    #print(all_abstracts)


    # Convert the list of abstracts into a pandas DataFrame
    data = pd.DataFrame(all_abstracts)
    #print(data)

    #Number of records grouped by the journal
    cnt = data.groupby(['Journal']).size()
    #print(cnt)

    #Convert count to df
    df = cnt.to_frame().reset_index()
    #print(df)

    df = df.rename(columns={0:'Total_articles'})
    #print(df)

    #Sort by article
    df = df.sort_values(by='Total_articles', ascending=False)
    #print(df)
    top_n= df.nlargest(n,'Total_articles')
    #print(top_n)
    return top_n



if __name__ == "__main__":
    top_journals()
