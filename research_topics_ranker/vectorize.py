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

from wordcloud import WordCloud
import matplotlib.pyplot as plt


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



if __name__ == "__main__":
    id_list = search_pubmed(query)
    all_abstracts = fetch_all_abstracts(id_list, nr_of_requests)

    # Convert the list of abstracts into a pandas DataFrame
    df_abstracts = pd.DataFrame(all_abstracts)

    df_abstracts['Clean_Abstract'] = df_abstracts['Abstract'].apply(clean)

    # Vectorizing the data
    vectorizer = TfidfVectorizer(ngram_range=(1, 3),
                                 min_df=0.05,
                                 max_df=0.95).fit(df_abstracts['Clean_Abstract'])

    vectors = pd.DataFrame(vectorizer.transform(df_abstracts['Clean_Abstract']).toarray(),
                           columns=vectorizer.get_feature_names_out())
    sum_tfidf = vectors.sum(axis=0)

    tfidf_list = [(word, sum_tfidf[word])
                  for word, idx in vectorizer.vocabulary_.items()]

    sorted_tfidf_list = sorted(tfidf_list, key=lambda x: x[1], reverse=True)


    # Convert the sorted TF-IDF list to a dictionary
    tfidf_dict = {word: score for word, score in sorted_tfidf_list}

    # Generate a word cloud image
    wordcloud = WordCloud(width = 800, height = 400,
                          background_color ='white',
                          max_words=500).generate_from_frequencies(tfidf_dict)

    # Display the generated image:
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
