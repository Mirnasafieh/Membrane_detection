from skimage import data
from skimage import color
from skimage.filters import meijering, sato, frangi, hessian
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
import skimage
import skimage.io 
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import feature
from PIL import Image, ImageEnhance
from skimage import data, exposure, img_as_float
from skimage.filters import unsharp_mask
import matplotlib.pyplot as plt
from cv2 import cv2
import matplotlib.patches as mpatches
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from skimage.util import img_as_ubyte
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from skimage.morphology import black_tophat, skeletonize, convex_hull_image
from skimage.morphology import disk
from scipy.ndimage import gaussian_filter
from scipy import misc
import matplotlib.pyplot as plt
from skimage import filters
from scipy import ndimage, misc
import scipy
from skimage import measure


def plot_comparison(original, filtered, filter_name):
    """plots two images together for comparison"""
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True,
                                   sharey=True)
    ax1.imshow(original, cmap=plt.cm.gray)
    ax1.set_title('original')
    ax1.axis('off')
    ax2.imshow(filtered, cmap=plt.cm.gray)
    ax2.set_title(filter_name)
    ax2.axis('off')

def grayschale(img):
    """converts the image into a grayscale"""
    original = skimage.io.imread(img)
    grayscale = rgb2gray(original)

    return grayscale

def sharpen(img):
    """sharpens the image"""
    result = unsharp_mask(img, radius=3, amount=3)
    return result

def edge_detec(img,sigma_val):
    """edge detection using skimage canny"""
    edges = feature.canny(img, sigma=sigma_val)
    return edges

def close_img (img):
    phantom = img
    phantom[10:30, 200:210] = 0
    selem = disk(6)
    closed = closing(phantom, selem)
    return closed 

def open_img (img):
    selem = disk(3)
    opened = opening(img, selem)
    return opened 

def dialate_img (img):
    selem = disk(3)
    dialated=dilation(opened_edge, selem)
    return dialated

def gaussian_filter_img (img):
    filtered=gaussian_filter(img, sigma=0.5)

    return filtered

def threshold_otsu_img(img):
    image = img
    val = filters.threshold_otsu(image)
    thresh=image < val
    return thresh

if __name__ == "__main__":
    # original = skimage.io.imread('new_image.tif')
    # plt.imshow(original, cmap = 'gray')
    # plt.title('original'), plt.xticks([]), plt.yticks([])
    # plt.show()

    im_gray=grayschale('new_image.tif')
    # plt.imshow(im_gray, cmap = 'gray')
    # plt.title('grayscale'), plt.xticks([]), plt.yticks([])
    # plt.show()
    
    im_sharp= sharpen(im_gray)
    # plt.imshow(im_sharp, cmap = 'gray')
    # plt.title('sharp'), plt.xticks([]), plt.yticks([])
    # plt.show()
    
    # edge_sobel = filters.sobel(im_sharp)
    # edge_sobel = scipy.ndimage.sobel(im_sharp, axis=-1, output=None, mode='reflect', cval=10)
    # plt.imshow(edge_sobel, cmap = 'gray')
    # plt.title('edge_sobel'), plt.xticks([]), plt.yticks([])
    # plt.show()

    opened_edge=edge_detec(im_sharp,0)
    # plt.imshow(opened_edge, cmap = 'gray')
    # plt.title('edge detection'), plt.xticks([]), plt.yticks([])
    # plt.show()

    # after_th = threshold_otsu_img(opened_edge)
    # plt.imshow(after_th, cmap = 'gray')
    # plt.title('after_th'), plt.xticks([]), plt.yticks([])
    # plt.show()
     
    dialated=dialate_img (opened_edge)
    # plt.imshow(dialated, cmap = 'gray')
    # plt.title('dialated'), plt.xticks([]), plt.yticks([])
    # plt.show()

    opened_edge_closed=close_img (dialated)
    # plt.imshow(opened_edge_closed, cmap = 'gray')
    # plt.title('opened_edge_closed'), plt.xticks([]), plt.yticks([])
    # plt.show()

    opened = open_img (opened_edge_closed)
    # plt.imshow(opened, cmap = 'gray')
    # plt.title('opened'), plt.xticks([]), plt.yticks([])
    # plt.show()

    filtered=gaussian_filter(opened, sigma=0)
    # plt.imshow(filtered, cmap = 'gray')
    # plt.title('gaussian_filter'), plt.xticks([]), plt.yticks([])
    # plt.show()

    after_th = threshold_otsu_img(filtered)
    plt.imshow(after_th, cmap = 'gray')
    plt.title('after_th'), plt.xticks([]), plt.yticks([])
    plt.show()



    # contours = measure.find_contours(filtered, 0.9)
    # fig, ax = plt.subplots()
    # ax.imshow(filtered, cmap=plt.cm.gray)

    # for n, contour in enumerate(contours):
    #     ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    # ax.axis('image')
    # ax.set_xticks([])
    # ax.set_yticks([])
    # plt.show()