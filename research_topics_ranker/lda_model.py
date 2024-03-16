import pandas as pd
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation

import matplotlib.pyplot as plt


def lda_model_fit(n_components, max_iter, vectorized_documents):
    lda_model = LatentDirichletAllocation(n_components=n_components, max_iter = max_iter)

    # Fit the LDA on the vectorized documents
    lda_model.fit(vectorized_documents)

    return lda_model


def topics_list(model, vectorizer, top_words):
    topics = []
    for idx, topic in enumerate(model.components_):
        # print("Topic %d:" % (idx))
        topic = [(vectorizer.get_feature_names_out()[i], topic[i]) for i in topic.argsort()[:-top_words - 1:-1]]
        # print(topic)
        topics.append(topic)
    return topics

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


def lda_model_transform(model, vectorized_documents, original_DF):
    # Return a DF that merges the original DF with the array that classify the topics
    document_topic_mixture = model.transform(vectorized_documents)
    R, T = document_topic_mixture.shape

    #create new column with the topic number
    max_indices = np.argmax(document_topic_mixture, axis=1)
    new_column = max_indices[:, np.newaxis]
    document_topic_mixture_cluster_n = np.concatenate((document_topic_mixture, new_column), axis=1)

    #transform the array to DF
    columns = ['topic_{}'.format(i) for i in range(3)] + ['Main_Topic']
    df_array = pd.DataFrame(document_topic_mixture_cluster_n, columns=columns)

    #merge original DataFrame with this
    merged_df = pd.concat([original_DF, df_array], axis=1)

    # meed to return the max column
    # return document_topic_mixture
    # return document_topic_mixture_cluster_n
    return merged_df
