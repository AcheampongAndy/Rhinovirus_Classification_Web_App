import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
import io
import base64

def plot_multiple_trees(distance_matrices, titles=None, **kwargs):
    """
    Plots dendrograms for multiple distance matrices.

    Args:
        distance_matrices (list of numpy.ndarray): A list of distance matrices.
        titles (list of str, optional): Titles for each dendrogram. Defaults to None.
        **kwargs: Additional arguments to pass to the dendrogram function.

    Returns:
        str: Base64-encoded PNG image of the plot.
    """
    num_matrices = len(distance_matrices)
    if titles is None:
        titles = [f"Dendrogram {i+1}" for i in range(num_matrices)]
    
    # Create a subplot grid
    fig, axes = plt.subplots(1, num_matrices, figsize=(5 * num_matrices, 5))
    
    # Handle single axis case
    if num_matrices == 1:
        axes = [axes]

    for i, (distance_matrix, title) in enumerate(zip(distance_matrices, titles)):
        # Convert the data to a numpy array (if not already)
        distance_matrix = np.array(distance_matrix)
        
        # Perform hierarchical clustering using complete linkage
        linkage_matrix = sch.linkage(distance_matrix, method='complete')
        
        # Plot the dendrogram
        sch.dendrogram(linkage_matrix, ax=axes[i], **kwargs)
        axes[i].set_title(title)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot to a BytesIO object and encode it as base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    
    return plot_url