import logging
import matplotlib.pyplot as plt
import numpy as np


def get_logger(name):
    logging.basicConfig(format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger


logger = get_logger(__name__)


def get_metadata_string(metadata, index):
    track = metadata[metadata['amazon-id'] ==  index]
    artist = track.artist.values[0]
    name = track.title.values[0]
    genre = track['root-genre'].values[0]
    return '{} - {} [{}]'.format(artist, name, genre)


def plot_topics(lda_model, i):
    
    name = 'Topic {}'.format(i)
    this_topic = lda_model.show_topic(i)
    
    terms = [x[0] for x in this_topic]
    weights = [x[1] for x in this_topic]
    
    plt.rcdefaults()
    fig, ax = plt.subplots()
    
    # Example data
    y_pos = np.arange(len(terms))
    
    ax.barh(y_pos, weights, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(terms)
    ax.invert_yaxis()
    ax.set_title(name)
    
    plt.show()