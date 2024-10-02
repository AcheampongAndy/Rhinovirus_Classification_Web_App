import numpy as np
from flaskr.utils.gaps import delete_missing_data_sites
from flaskr.utils.trans_pro import calc_transition_transversions

def calc_kimura_2p_distance(sequences, headers, gap_deletion=True):
    if gap_deletion:
        sequences = delete_missing_data_sites(sequences)

    k2p_matrix = np.full((len(headers), len(headers)), np.nan)

    # Iterate over each pair of sequence
    for i, seq1 in enumerate(sequences):
        for j, seq2 in enumerate(sequences):
            if len(seq1) == len(seq2):

                P, Q = calc_transition_transversions(seq1, seq2)

                if (1 - 2*P - Q) > 0 and (1 - 2*Q) > 0:
                    k2p_matrix[i, j] = -0.5 * np.log((1 - 2*P - Q) * np.sqrt(1 -2*Q))

    return k2p_matrix