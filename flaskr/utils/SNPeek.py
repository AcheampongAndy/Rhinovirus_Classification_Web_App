import matplotlib
matplotlib.use('agg') 
import matplotlib.pyplot as plt
import io
import base64

def SNPeek(sequences, headers, show_legend=False):
    genome_length = max(len(seq) for seq in sequences)

    def compare_sequences(seqA, seqB):
        differences = [(i, seqB[i]) for i in range(len(seqA)) if seqA[i] != seqB[i]]

        return differences
    
    color_map = {'A': 'green', 'T': 'red', 'G': 'blue', 'C': 'yellow'}

    diff_list = []
    for i in range(1, len(sequences)):
        diffs = compare_sequences(sequences[0], sequences[i])
        diff_list.append([(pos, color_map.get(sub_type, 'black')) for pos, sub_type in diffs])

    fig, ax = plt.subplots()
    ax.set_xlim(0, genome_length)
    ax.set_ylim(0.5, len(sequences))
    ax.set_xlabel(f"Genome position of {headers[0]}, acting as reference")
    ax.set_ylabel("Sequences")

    ax.set_yticks(range(1, len(headers) + 1))
    ax.set_yticklabels(headers)

    for i, diffs in enumerate(diff_list):
        for pos, color in diffs:
            ax.vlines(pos, i + 0.75, i + 1.25, color=color)

    if show_legend:
        legend_labels = [plt.Line2D([0], [0], color=c, lw=2) for c in color_map.values()]
        ax.legend(legend_labels, color_map.keys(), loc='upper left', bbox_to_anchor=(1, 1))


    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return plot_url