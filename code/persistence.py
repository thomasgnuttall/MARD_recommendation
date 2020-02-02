import pandas as pd
import pickle

import utils

logger = utils.get_logger('__main__')


def combine_reviews(data):

    df = data[['amazon-id', 'reviewText']]\
            .groupby('amazon-id')['reviewText']\
            .apply(' '.join)\
            .reset_index()
    logger.info('Combined {} reviews to {}'.format(len(data), len(df)))
    return df


def load_data(path):
	"""
	Load MARD review JSON at <path>
	Return pandas.DataFrame
	"""
	logger.info('Loading review data from {}'.format(path))

	data = pd.read_json(path, lines=True)
	
	num_reviews = len(data)
	num_albums = len(set(data['amazon-id']))
	num_reviewers = len(set(data['reviewerID']))

	logger.info(
		'{} reviews of {} albums by {} reviewers'\
		.format(num_reviews, num_albums, num_reviewers)
	)

	return data


def pickle_object(filepath, thing_to_pickle):
    outfile = open(filepath, 'wb')
    pickle.dump(thing_to_pickle, outfile)
    outfile.close()


def load_pickle(path):
    with open(path, "rb") as f:
        l = pickle.load(f)
    return l


def load_folder(folder):
    lda_model = gensim.models.LdaModel.load('{}/model'.format(folder))
    gen_dict = gensim.corpora.Dictionary.load('{}/dict'.format(folder))
    corpus = load_pickle('{}/corpus.pkl'.format(folder))
    amazon_ids = load_pickle('{}/amazon_ids.pkl'.format(folder))
    
    return lda_model, gen_dict, corpus, amazon_ids