import numpy as np
from flaskr.utils.count_snp import count_snps_helper
from flaskr.utils.gaps import delete_missing_data_sites

def calc_p_distance(sequences, headers, gap_deletion=True):
    snp_counts = count_snps_helper(sequences, headers, gap_deletion)

    if gap_deletion:
        sequences = delete_missing_data_sites(sequences)

    seq_lengths = [len(seq) for seq in sequences]

    # prepare matrix for p distance
    p_distance_matrix = np.full((len(headers), len(headers)), np.nan)

    # Calculate p distance
    for i in range(len(headers)):
        for j in range(len(headers)):
            if not np.isnan(snp_counts[i, j]):
                p_distance_matrix[i, j] = snp_counts[i, j] / seq_lengths[i]

    
    return p_distance_matrix