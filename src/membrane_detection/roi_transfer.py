from skimage.color import rgb2gray
import skimage
from skimage import feature
import numpy as np
from skimage.filters import unsharp_mask
import matplotlib.pyplot as plt
import skimage.io 
import cv2
import numpy as np
from matplotlib import pyplot as plt
import skimage
import skimage.io
from skimage import data, util, measure
import pandas as pd
import imagecodecs
import tifffile
from skimage.color import rgb2gray
import skimage.segmentation as seg
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
import argparse
from skimage import feature


def grayschale(img):
    """converts the image into a grayscale"""
    original = skimage.io.imread(img)
    grayscale = rgb2gray(original)

    return grayscale


def sharpen(img):
    """sharpens the image"""
    result = unsharp_mask(img, radius=2, amount=2)
    return result


def edge_detec(img, sigma_val):
    """edge detection using skimage canny"""
    edges = feature.canny(img, sigma=sigma_val)
    return edges


def image_measurements(img):
    results_dict = {}
    total_area = img.size
    stained_area = np.count_nonzero(img)
    percent_area = stained_area / total_area
    total_intensity = np.sum(img)
    mean_intensity = np.mean(img)
    intigrated_optical_density = mean_intensity * stained_area   # check math
    results_dict.update({"total area:", total_area, "stained area:", stained_area, "percent area:", percent_area,
        "total_intensity:", total_intensity, "mean_intensity:", mean_intensity, "intigrated_optical_density:", intigrated_optical_density })
    df = pd.DataFrame.from_dict(results_dict, orient='index')


def compare_images(img1, img2):
    compare_im = np.copy(img2)
    compare_im = np.where(img1 == False, 0, compare_im)
    return (compare_im)

if __name__ == "__main__":
    original = skimage.io.imread("image-0.tif")
    gray_image = grayschale("image-0.tif")
    sharp_image = sharpen(gray_image)
    bf_im = edge_detec(sharp_image, 0.5)
    fl_im = grayschale("image-1.tif")
    new = compare_images(bf_im, fl_im)
    new_im = rgb2gray(new)

    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, figsize=(8, 8))
    axes = axes.ravel()

    axes[0].imshow(original, cmap=plt.cm.gray)
    axes[0].set_title('Original image')

    axes[1].imshow(bf_im, cmap=plt.cm.gray)
    axes[1].set_title('BF image')

    axes[2].imshow(fl_im, cmap=plt.cm.gray)
    axes[2].set_title('fluorescent image')

    axes[3].imshow(new_im, cmap=plt.cm.gray)
    axes[3].set_title('comparison image')

    for ax in axes:
        ax.axis('off')

    plt.tight_layout()
    plt.show()
    # image_measurements(new)