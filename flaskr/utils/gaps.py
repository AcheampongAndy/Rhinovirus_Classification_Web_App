import numpy as np

def delete_missing_data_sites(sequences):
    # Convert sequences to a numpy array where each sequence is a row
    seq_matrix = np.array([list(seq) for seq in sequences])

    # Find columns that do not contain gaps ('-' is the gap)
    valid_columns = ~np.any(seq_matrix == '-', axis=0)

    # Keep only valid columns
    cleaned_matrix = seq_matrix[:, valid_columns]

    # Convert the cleaned matrix back to a list of sequence
    cleaned_seqs = [''.join(row) for row in cleaned_matrix]

    return cleaned_seqs