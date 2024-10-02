import numpy as np
from flaskr.utils.gaps import delete_missing_data_sites

def count_snps_helper(sequences, headers, gap_deletion=True):
    if gap_deletion:
        sequences = delete_missing_data_sites(sequences)

    # Convert all sequences into a matrix of characters
    seq_matrix = np.array([list(seq) for seq in sequences])

    # Initialize SNP matrix
    snp_matrix = np.full((len(headers), len(headers)), np.nan)

    # Calculate SNP for all pairs of sequence
    for i in range(len(seq_matrix)):
        for j in range(i, len(seq_matrix)):
            snps = np.sum(seq_matrix[i] != seq_matrix[j])
            snp_matrix[i, j] = snp_matrix[j, i] = snps

    
    return snp_matrix