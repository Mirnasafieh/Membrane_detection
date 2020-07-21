import numpy as np
import matplotlib.pyplot as plt
from skimage import filters
from skimage.data import camera
from skimage.util import compare_images
import skimage
import skimage.io
from skimage.color import rgb2gray


def edges (im):
    original = skimage.io.imread(im)
    grayscale = rgb2gray(original)
    edge_sobel = filters.sobel(grayscale)
    edge_scharr = filters.scharr(grayscale)
    edge_prewitt = filters.prewitt(grayscale)

    diff_scharr_prewitt = compare_images(edge_scharr, edge_prewitt)
    diff_scharr_sobel = compare_images(edge_scharr, edge_sobel)
    max_diff = np.max(np.maximum(diff_scharr_prewitt, diff_scharr_sobel))

    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True,
                            figsize=(8, 8))
    axes = axes.ravel()

    # axes[0].imshow(im, cmap=plt.cm.gray)
    # axes[0].set_title('Original image')

    axes[1].imshow(edge_scharr, cmap=plt.cm.gray)
    axes[1].set_title('Scharr Edge Detection')

    axes[2].imshow(diff_scharr_prewitt, cmap=plt.cm.gray, vmax=max_diff)
    axes[2].set_title('Scharr - Prewitt')

    axes[3].imshow(diff_scharr_sobel, cmap=plt.cm.gray, vmax=max_diff)
    axes[3].set_title('Scharr - Sobel')

    for ax in axes:
        ax.axis('off')

    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    edges('image-0.tif')