import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_kernels

import utils

logger = utils.get_logger('__main__')

def train_tfidf(word_reviews):
	"""
	Extract count features, apply TF-IDF normalisation and row-wise euclidean normalization
	using sklearns TF-IDF vectorizer
	"""

	# Sklearn expects paragraphs rather than words list
	logger.info('Building paragraphs from word list and fitting TF-IDF')
	paragraphs = [' '.join(w) for w in word_reviews]
	return TfidfVectorizer().fit_transform(paragraphs)


def predict_topic_distribution(lda_model, corpus):
    """
    Use gensim lda_model, <lda_model> to predict topic distributions of <corpus>
    Returns: np.array
    	probability vector of length=number of topics
    """
    num_topics = lda_model.num_topics
    logger.info('Predicting on {} documents across {} topics'\
    				.format(corpus, num_topics))
    predict = lda_model.get_document_topics(corpus)
    final_predict = []
    for dis in predict:
        this_dis = np.zeros(num_topics)
        for t,d in dis:
            this_dis[t] = d
        final_predict.append(this_dis)
    return final_predict


def recommender(distance_matrix, indices, index, n=5):
    """
    Given a square matrix of cosine similarities, <distance_matrix>
    ...with <indices>
    Return list of top n most similar indices for <index>
    """
    i = indices.index(index)
    row = enumerate(distance_matrix[i])
    top_n = sorted(row, key=lambda y: y[1], reverse=True)[1:n+1]
    return [(indices[i],j) for i,j in top_n]


def get_rec_from_substring(s, metadata, LDA_sim, amazon_ids):
    """
    Search artists for matches of <s>, randomly select album and print top 5 recommendations.
    if s = None: select random
    """
    if s:
        this_artist = [(x,i) for x,i in zip(metadata['artist'], metadata['amazon-id']) if isinstance(x, str)]
        try:
            test_id = random.choice([x[1] for x in this_artist if s.lower() in x[0].lower()])
        except Exception as e:
            print(e)
            print('Substring not matched! Try Another...')
            return
    else:
        test_id = random.choice(amazon_ids)
    recs = [
        (utils.get_metadata_string(metadata, x[0])) \
         for x in recommender(LDA_sim, amazon_ids, test_id)
    ]
    print("Top Recommendations for {}:\n"\
          .format(utils.get_metadata_string(metadata, test_id)))
    for r in recs:
        print(r)

