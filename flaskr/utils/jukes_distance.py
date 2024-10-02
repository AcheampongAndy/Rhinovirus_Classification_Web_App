import numpy as np
from flaskr.utils.p_distance import calc_p_distance

def calc_jukes_cantor_distance(sequences, heaeders, gap_deletion=True):
    p_dist = calc_p_distance(sequences, heaeders, gap_deletion)

    # Juke Cantor distance matrix
    jc_dist = np.full(p_dist.shape, np.nan)

    # Apply Juke Cantor formula
    with np.errstate(divide='ignore', invalid='ignore'):
        jc_dist = -3/4 * np.log(1 - 4/3 * p_dist)


    # Handle cases where p-distance >= 0.75
    jc_dist[p_dist >= 0.75] = np.inf

    return jc_dist