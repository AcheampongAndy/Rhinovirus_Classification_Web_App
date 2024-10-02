from Bio import SeqIO

# Function 1
# Compare lengths among input sequences and pad short sequences with "-" until they are as long as the longest sequence
def compare_lengths(seqs):
    # Find the maximum sequence length
    max_length = max(len(seq) for seq in seqs.values())
    print(f"Max sequence length: {max_length}")
    
    # Adjust sequences to match the longest length by padding with "-"
    adjusted_seqs = {header: seq + '-' * (max_length - len(seq)) if len(seq) < max_length else seq 
                     for header, seq in seqs.items()}
    
    # Print lengths after adjustment
    for header, seq in adjusted_seqs.items():
        print(f"Length of {header}: {len(seq)}")
    
    return adjusted_seqs


# Function 2
# Read sequences from a FASTA file and adjust their lengths
def read_fasta(fasta_file):
    # Read sequences from a FASTA file
    alignment = SeqIO.parse(fasta_file, "fasta")
    
    # Convert the sequences to a dictionary with headers as keys and sequences as values
    seq_dict = {record.id: str(record.seq) for record in alignment}

    # Print sequence lengths before adjustment
    for header, seq in seq_dict.items():
        print(f"Original length of {header}: {len(seq)}")
    
    # Adjust all sequences to the length of the longest sequence
    adjusted_seq_dict = compare_lengths(seq_dict)
    
    # Return the adjusted sequences
    return adjusted_seq_dict
