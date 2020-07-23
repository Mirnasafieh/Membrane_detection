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
from tifffile import imsave

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
    result = unsharp_mask(img, radius=2, amount=2)
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
    im_gray=grayschale('image-0.tif')
    im_sharp= sharpen(im_gray)

    filtered=gaussian_filter(im_sharp, sigma=1)
    plot_comparison(im_sharp, filtered, 'opened1')

    opened = open_img (filtered)
    plot_comparison(filtered, opened, 'opened1')

    opened_edge=edge_detec(opened,0.5)
    plot_comparison(opened, opened_edge, 'edgedetec2')

    dialated=dialate_img (opened_edge)
    plot_comparison(opened_edge, dialated, 'dialated3')

    opened_edge_closed=close_img (dialated)
    
    plot_comparison(opened_edge, opened_edge_closed, 'closed4')

    plot_comparison(im_sharp, opened_edge_closed, 'final')

    plt.show()
    





    # """ the following code recognized subpopulations in the picture, maybe we could use it to eliminate them and clean the picture"""
    # image = im3

    # # apply threshold
    # thresh = threshold_otsu(image)
    # bw = closing(image > thresh, square(3))

    # # remove artifacts connected to image border
    # cleared = clear_border(bw)

    # # label image regions
    # label_image = label(cleared)
    # # to make the background transparent, pass the value of `bg_label`,
    # # and leave `bg_color` as `None` and `kind` as `overlay`
    # image_label_overlay = label2rgb(label_image, image=image, bg_label=0)

    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.imshow(image_label_overlay)

    # for region in regionprops(label_image):
    #     # take regions with large enough areas
    #     if region.area >= 100:
    #         # draw rectangle around segmented coins
    #         minr, minc, maxr, maxc = region.bbox
    #         rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
    #                                 fill=False, edgecolor='red', linewidth=2)
    #         ax.add_patch(rect)

    # ax.set_axis_off()
    # plt.tight_layout()
    # plt.show()

