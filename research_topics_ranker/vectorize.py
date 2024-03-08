from research_topics_ranker.fetch_data import search_pubmed, fetch_all_abstracts
from research_topics_ranker.params import *
import pandas as pd

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import unidecode
nltk.download('punkt')
nltk.download('stopwords')


api_key = EUTILS_API_KEY        # It's recommended to include your NCBI API key
email = EMAIL
query = QUERY
nr_of_requests = NR_OF_REQUESTS

def clean (text):

    #print(text)
    if text is None:
        return ""  # Return an empty string if the text is None

    for punctuation in string.punctuation:
        text = text.replace(punctuation, ' ') # Remove Punctuation

    lowercased = text.lower() # Lower Case

    unaccented_string = unidecode.unidecode(lowercased) # remove accents

    tokenized = word_tokenize(unaccented_string) # Tokenize

    words_only = [word for word in tokenized if word.isalpha()] # Remove numbers

    stop_words = set(stopwords.words('english')) # Make stopword list

    without_stopwords = [word for word in words_only if not word in stop_words] # Remove Stop Words

    return " ".join(without_stopwords)

id_list = search_pubmed(query)
all_abstracts = fetch_all_abstracts(id_list, nr_of_requests)

# Convert the list of abstracts into a pandas DataFrame
df_abstracts= pd.DataFrame(all_abstracts)

df_abstracts['Clean_Abstract'] = df_abstracts['Abstract'].apply(clean)
#print(df_abstracts)

#Vectorizing the data
vectorizer = TfidfVectorizer(ngram_range=(2, 2),
                             min_df=0.01,
                             max_df=0.05).fit(df_abstracts['Clean_Abstract'])

vectors = pd.DataFrame(vectorizer.transform(df_abstracts['Clean_Abstract']).toarray(),
                       columns=vectorizer.get_feature_names_out())
#print(vectors)


sum_tfidf = vectors.sum(axis = 0)
#print(sum_tfidf)

tfidf_list = [(word, sum_tfidf[word])
              for word, idx in vectorizer.vocabulary_.items()]
#print(tfidf_list)

sorted_tfidf_list =sorted(tfidf_list, key = lambda x: x[1], reverse=True)
#print(sorted_tfidf_list)
