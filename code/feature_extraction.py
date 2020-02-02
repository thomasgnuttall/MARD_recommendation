import utils

logger = utils.get_logger('__main__')

import gensim
import nltk
import multiprocessing
import re
import spacy

nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('english')

nltk.download('words')
words = set(nltk.corpus.words.words())

nlp = spacy.load('en', disable=['parser', 'ner'])
allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']

meaningful_words=[]
with open("../data/meaningful_words.txt", "r") as f:
    for line in f:
        meaningful_words.append(line.replace('\n', ''))

meaningful_words = set(meaningful_words)


def parse_reviews(data):
    """
    Extract word features from corpus of reviews
    """
    logger.info('Parsing reviews and extracting meaningful words')
    pool = multiprocessing.Pool()
    word_reviews = pool.map(extract_words, data)

    # Some reviews have no words that satisfy our requirement
    word_reviews = [x for x in word_reviews if x[1]]
    all_words = [y for x in word_reviews for y in x[1]]
    logger.info('Total number of unique words in corpus {}'\
                    .format(len(set(all_words))))
    return word_reviews


def extract_words(s_):
    """
    Extract and filter meaningful words from paragraph string
    <s_> = <amazon-id>, <review>
    """

    amazon_id, s = s_

    # Remove apostrophes
    s = s.replace("'", "")

    # Get word list
    l = re.compile('[A-Za-z]+').findall(s)

    # Force to lower case
    l = [x.lower() for x in l]
    
    # Remove stopwords
    stop_words_no_punc = [x.replace("'", "") for x in stop_words]
    l = [x for x in l if x not in stop_words_no_punc]

    # Remove small words
    l = [x for x in l if len(x) > 2]

    # Remove non-words
    l = list(set(l).intersection(meaningful_words))

    return amazon_id, l


def apply_gram_models(word_reviews_id, min_count=5, threshold=100):
    """
    Train bigram and trigram models on <word_reviews>
    Returning transformed word_reviews
    """
    amazon_id  = [x[0] for x in word_reviews_id]
    word_reviews = [x[1] for x in word_reviews_id]

    logger.info('Training bigram and trigram models')
    bigram = gensim.models.Phrases(
        word_reviews, min_count=min_count, threshold=threshold)
    bigram_reviews = bigram[word_reviews]
    trigram = gensim.models.Phrases(bigram_reviews, threshold=threshold)  
    return zip(amazon_id, list(trigram[bigram_reviews]))
    

def compute_lemmas(input_):
    amazon_id, review = input_
    doc = nlp(" ".join(review))
    return amazon_id, [token.lemma_ for token in doc if token.pos_ in allowed_postags]


def lemmatization(wr):
    """
    Identify lemmas and transform all reviews
    """
    pool = multiprocessing.Pool()
    results = pool.map(compute_lemmas, wr)
    return results


def get_dict_and_corpus(word_reviews_id):
    """
    Indicize review corpus and return dictionary and corpus
    """
    amazon_id = [x[0] for x in word_reviews_id]
    word_reviews = [x[1] for x in word_reviews_id]
    gen_dict = gensim.corpora.Dictionary(word_reviews)
    corpus = [gen_dict.doc2bow(review) for review in word_reviews]
    return amazon_id, gen_dict, corpus
