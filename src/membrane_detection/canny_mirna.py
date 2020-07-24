from skimage.filters import meijering, sato, frangi, hessian, threshold_otsu, rank, unsharp_mask
import matplotlib.pyplot as plt
from skimage.color import rgb2gray, label2rgb
import skimage
import skimage.io 
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageEnhance
from skimage import data, exposure, img_as_float, morphology, filters, feature, color
from cv2 import cv2
import matplotlib.patches as mpatches
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.util import img_as_ubyte
from skimage.morphology import erosion, dilation, opening, closing, white_tophat, flood_fill, black_tophat, skeletonize, convex_hull_image, disk, closing, square
from scipy.ndimage import gaussian_filter
from scipy import misc
from tifffile import imsave
from skimage.util.dtype import dtype_range


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
    selem = disk(10)
    closed = closing(phantom, selem)
    return closed 

def open_img (img):
    selem = disk(3)
    opened = opening(img, selem)
    return opened 

def dialate_img (img):
    selem = disk(4)
    dialated=dilation(img, selem)
    return dialated

def gaussian_filter_img (img):
    filtered=gaussian_filter(img, sigma=0.5)

    return filtered

def threshold_otsu_img(img):
    image = img
    val = filters.threshold_otsu(image)
    thresh=image < val
    return thresh

def bf_prep(img):
    
if __name__ == "__main__":
    im_gray=grayschale('new_image_4.tif')
    im_sharp= sharpen(im_gray)

    """option 1"""

    #gray scale picture:
    img = im_sharp

    # Equalization threshold:
    p2, p98 = np.percentile(img, (2, 98))
    a = exposure.rescale_intensity(im_gray, in_range=(p2, p98))
    plot_comparison(im_sharp, a, 'equalize')
    plt.show()

    #Gaussian:
    b=gaussian_filter(a, sigma=2.7)
    plot_comparison(a, b, 'gaussian')
    plt.show()

    #Edge detection: 
    d=edge_detec(b,1)
    plot_comparison(b, d, 'edge')
    plt.show()

    #remove small objects:
    e = morphology.remove_small_objects(d, 200, in_place=True, connectivity=50)
    plot_comparison(d, e, 'remove small objects')
    plt.show()

    #close:
    f=close_img (e)
    plot_comparison(e, f, 'close')
    plt.show()

    #dialated:
    g=dialate_img (f)
    plot_comparison(img, g, 'dialated')
    plt.show()


    #remove small objects:
    h = morphology.remove_small_objects(g, 1700, in_place=True, connectivity=200)
    plot_comparison(img, h, 'remove small objects')
    plt.show()


