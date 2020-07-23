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
    # print(np.argwhere(img1 == True))
    # new_compare = np.logical_and(edge_image, edge_image2, out=None, where=True, casting='same_kind', order='K', dtype=None, subok=True)
    # return new_compare

if __name__ == "__main__":
    gray_image = grayschale("new_image.tif")
    sharp_image = sharpen(gray_image)
    edge_image = edge_detec(sharp_image, 0.5)
    plt.imshow(edge_image, cmap = 'gray')
    plt.title('1st image'), plt.xticks([]), plt.yticks([])
    plt.show()
    gray_image2 = grayschale("new_image.tif")
    sharp_image2 = sharpen(gray_image2)
    edge_image2 = edge_detec(sharp_image2, 0.5)
    plt.imshow(edge_image2, cmap = 'gray')
    plt.title('2nd image'), plt.xticks([]), plt.yticks([])
    plt.show()
    compare_images(edge_image, edge_image2) 
    # plt.imshow(new, cmap = 'gray')
    # plt.title('comparison image'), plt.xticks([]), plt.yticks([])
    # plt.show()
    # image_measurements(new)