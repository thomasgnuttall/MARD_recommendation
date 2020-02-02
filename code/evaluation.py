from scipy.special import beta
from math import log, exp
import random

import model
import utils

logger = utils.get_logger('__main__')




def chance_deathmatch(metadata, LDA_sim, amazon_ids, chance, our_model):
    """
    Expects to globals to be defined, 'chance' and 'our_model'

    Asks the user to choose between two competing algorithms
    """
    # Randomly pick track
    test_id = random.choice(amazon_ids)
    track_name = utils.get_metadata_string(metadata, test_id)
    
    print('Recommendations for {}:\n'.format(track_name))
    
    # Generate two sets of recs
    model_recs = [
        (utils.get_metadata_string(metadata, x[0])) \
         for x in model.recommender(LDA_sim, amazon_ids, test_id)
    ]
    
    chance_recs = [
        utils.get_metadata_string(metadata, x) 
        for x in random.sample(amazon_ids, 5)
    ]
    
    all_recs = [(chance_recs, 'chance'), (model_recs, 'our_model')]
    random.shuffle(all_recs)
    
    d = {'A': all_recs[0], 'B': all_recs[1]}
    
    # FIGHT!
    for k in ['A', 'B']:
        V = d[k]
        print('Recommender {}:'.format(k))
        for v in V[0]:
            print(v)
        print('\n')
    
    result = input(['Which recommender is best, a or b? (or p to pass)']).upper()
    if not result == 'P':
        winner = d[result][1]
        if winner == 'chance':
            chance += 1
        else:
            our_model += 1

    return chance, our_model

            
def bayesian_test(alpha_A, beta_A, alpha_B, beta_B):
    """
    See: https://salasboni.wordpress.com/2015/02/06/online-formula-bayesian-ab-testing/
    and: https://www.evanmiller.org/bayesian-ab-testing.html
    """
    prob_pB_greater_than_pA = 0
    for i in range(0, alpha_B):
        prob_pB_greater_than_pA += exp(log(beta(alpha_A + i, beta_B + beta_A)) - \
    log(beta_B + i) - log(beta(1 + i, beta_B)) - log(beta(alpha_A, beta_A)))
    return prob_pB_greater_than_pA