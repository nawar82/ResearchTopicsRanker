from research_topics_ranker.fetch_data import *
from research_topics_ranker.params import *
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
import string
nltk.download('punkt', download_dir="/home/appuser/nltk_data")
nltk.download('stopwords', download_dir="/home/appuser/nltk_data")


from wordcloud import WordCloud
import matplotlib.pyplot as plt


api_key = EUTILS_API_KEY        # It's recommended to include your NCBI API key
email = EMAIL
query = QUERY
nr_of_requests = NR_OF_REQUESTS

def preprocessing(sentence):
    if sentence is None:
        return ""

    # remove whitespace
    sentence = sentence.strip()

    # lowercase characters
    sentence = sentence.lower()

    # remove numbers
    sentence = ''.join(char for char in sentence if not char.isdigit())

    # remove punctuation
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '')

    # remove stop_words
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(sentence)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    sentence = ' '.join(filtered_words)

    # tokenize and lemmatize
    words = word_tokenize(sentence)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, pos='v') for word in words]  # Lemmatize verbs
    lemmatized_words = [lemmatizer.lemmatize(word, pos='n') for word in lemmatized_words]  # Lemmatize nouns

    return ' '.join(lemmatized_words)


if __name__ == "__main__":
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

    tfidf_list = [(word, sum_tfidf[word])for word, idx in vectorizer.vocabulary_.items()]

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
