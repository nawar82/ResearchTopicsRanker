import pandas as pd

# ML Modules
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Graphs
import matplotlib.pyplot as plt

from research_topics_ranker.fetch_data import *
from research_topics_ranker.vectorize import *

from research_topics_ranker.params import *

api_key = EUTILS_API_KEY        # It's recommended to include your NCBI API key
email = EMAIL
query = QUERY
nr_of_requests = NR_OF_REQUESTS
n_components = N_COMPONENETS
max_iter = MAX_ITER


# Generate a word cloud image
def gen_wordcloud(worddict):
    wordcloud = WordCloud(width = 800, height = 400,
                        background_color ='white',
                        max_words=500).generate_from_frequencies(worddict)

    # Display the generated image:
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def lda_model_fit(n_components, max_iter, vectorized_documents):
    lda_model = LatentDirichletAllocation(n_components = n_components, max_iter = max_iter)
    lda_model.fit(vectorized_documents)
    return lda_model

def topics_list(model, vectorizer, n_components):
    topics = []
    for idx, topic in enumerate(model.components_):
        # print("Topic %d:" % (idx))
        topic = [(vectorizer.get_feature_names_out()[i], topic[i]) for i in topic.argsort()[:-n_components - 1:-1]]
        # print(topic)
        topics.append(topic)
    return topics

def plot_top_unique_words(topic_lists):
    # Combine all the lists into one
    combined_list = [item for sublist in topic_lists for item in sublist]

    # Sort the combined list by scores in descending order
    combined_list.sort(key=lambda x: x[1], reverse=True)

    # Filter out duplicates
    unique_words = {}
    for word, score in combined_list:
        if word not in unique_words:
            unique_words[word] = score

    # Extract the top 10 unique words and their scores
    top_words = list(unique_words.items())[:20]
    words, scores = zip(*top_words)

    # Step 5: Plot
    plt.figure(figsize=(10, 8))
    plt.barh(words, scores, color='skyblue')
    plt.xlabel('Scores')
    plt.title(f'Top 20 Unique Words Across all {n_components} Topics')
    plt.gca().invert_yaxis()  # To display the highest score at the top
    plt.show()

def graph_topics(topics):
    # Calculating the number of rows and columns
    num_sets = len(topics)
    num_cols = 2  # Number of columns you want
    num_rows = -(-num_sets // num_cols)  # Ceiling division to ensure enough rows

    # Plotting each data set
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))
    for i, data in enumerate(topics):
        row = i // num_cols
        col = i % num_cols
        labels = [item[0] for item in data]
        values = [item[1] for item in data]
        axs[row, col].barh(labels, values, color='skyblue')
        axs[row, col].set_ylabel('Keywords')
        axs[row, col].set_title('Topic {}'.format(i))
        axs[row, col].invert_yaxis()

    plt.xlabel('Score')
    plt.tight_layout()
    plt.show()



# need function that clasify every abstract in its category
def lda_model_transform(model, vectorized_documents):
    document_topic_mixture = model.transform(vectorized_documents)

    # meed to return the max column
    return document_topic_mixture


if __name__ == "__main__":
    # Search Pubmed and retreive the abstracts
    id_list = search_pubmed(query)
    all_abstracts = fetch_all_abstracts(id_list, nr_of_requests)

    # Convert the list of abstracts into a pandas DataFrame
    data = pd.DataFrame(all_abstracts)
    data['clean_text'] = data['Abstract'].apply(preprocessing)

    # Vectorizing the data
    vectorizer = TfidfVectorizer(ngram_range=(2, 3),
                                max_df=0.6).fit(data['clean_text'])

    #vectorized_documents = vectorizer.fit_transform(data['clean_text'])

    vectorized_documents = pd.DataFrame(vectorizer.transform(data['clean_text']).toarray(),
                                        columns=vectorizer.get_feature_names_out())
    sum_tfidf = vectorized_documents.sum(axis=0)

    tfidf_list = [(word, sum_tfidf[word]) for word, idx in vectorizer.vocabulary_.items()]

    sorted_tfidf_list = sorted(tfidf_list, key=lambda x: x[1], reverse=True)


    # Convert the sorted TF-IDF list to a dictionary
    tfidf_dict = {word: score for word, score in sorted_tfidf_list}

    #gen_wordcloud(tfidf_dict)

    lda_model = lda_model_fit(n_components=n_components,
                            max_iter = max_iter,
                            vectorized_documents = vectorized_documents)

    document_topic_mixture = pd.DataFrame(lda_model.transform(vectorized_documents),
                                        columns = [f"topic_{i}" for i in range(1, n_components+1)],
                                        index = data['PMID'])

    topics = topics_list(lda_model, vectorizer, n_components)

    plot_top_unique_words(topics)
    graph_topics(topics)
