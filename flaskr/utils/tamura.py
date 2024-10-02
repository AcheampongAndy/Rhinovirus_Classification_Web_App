import numpy as np
from flaskr.utils.gaps import delete_missing_data_sites
from flaskr.utils.trans_pro import calc_transition_transversions

def calc_tamura_3p_distance(sequences, headers, gap_deletion=True):
    if gap_deletion:
        sequences = delete_missing_data_sites(sequences)

    tamura_matrix = np.full((len(headers), len(headers)), np.nan)

    for i, seq1 in enumerate(sequences):
        for j, seq2 in enumerate(sequences):
            if len(seq1) == len(seq2):
                P, Q = calc_transition_transversions(seq1, seq2)
                gc_content_ref = sum(c in 'GC' for c in seq1) / len(seq1)
                gc_content_query = sum(c in 'GC' for c in seq2) / len(seq2)

                C = gc_content_ref + gc_content_query - 2 * gc_content_ref * gc_content_query

                if (1 - P/C - Q) > 0 and (1 - 2*Q) > 0:
                    tamura_matrix[i, j] = -C * np.log(1 - P/C - Q) - 0.5 * (1 - C) * np.log(1 - 2*Q)

        
    return tamura_matrix