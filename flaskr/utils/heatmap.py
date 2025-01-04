import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def plot_heatmap(distance_matrix, figsize=(10, 8), cmap='coolwarm', cbar=True):
    """
    Plot a heatmap of the given distance matrix with improved readability.

    Args:
        distance_matrix (array-like): The distance matrix to plot.
        figsize (tuple): Figure size for the heatmap.
        cmap (str): Colormap for the heatmap.
        cbar (bool): Whether to display a color bar.

    Returns:
        str: Base64-encoded string of the heatmap image.
    """
    # Ensure the distance_matrix is a numpy array
    distance_matrix = np.array(distance_matrix)

    # Check for NaN or infinite values and handle them
    if not np.all(np.isfinite(distance_matrix)):
        raise ValueError("The distance matrix contains non-finite values (NaN or Inf).")

    # Create the heatmap plot
    plt.figure(figsize=figsize)
    sns.heatmap(
        distance_matrix,
        cmap=cmap,
        cbar=cbar,
        xticklabels=10,  # Show every 10th label on x-axis
        yticklabels=10,  # Show every 10th label on y-axis
        square=True,  # Ensure cells are square
    )

    # Save the plot to a BytesIO object and encode it as base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')  # Adjust for better cropping
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return plot_url