def calc_transition_transversions(ref_chars, query_chars):
    transitions = sum((ref == 'A' and query == 'G') or
                      (ref == 'G' and query == 'A') or
                      (ref == 'C' and query == 'T') or
                      (ref == 'T' and query == 'C') for ref, query in zip(ref_chars, query_chars))
    
    transversions = sum((ref == 'A' and query in ['C', 'T']) or
                        (ref == 'G' and query in ['C', 'T']) or
                        (ref == 'C' and query in ['A', 'G']) or
                        (ref == 'T' and query in ['A', 'G']) for ref, query in zip(ref_chars, query_chars))
    
    total_sites = len(ref_chars)
    P = transitions / total_sites
    Q = transversions / total_sites


    return P, Q