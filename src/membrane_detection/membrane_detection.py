import matplotlib.pyplot as plt
import skimage
import skimage.io 
from skimage.filters import meijering, sato, frangi, hessian, threshold_otsu, rank, unsharp_mask
from skimage.color import rgb2gray, label2rgb
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

def membrane_detect(img_grayscale):
    """This fuction detects the membrane from a series of manipulations on a grayscale bright-field image"""
    """input: grayscale image"""
    """output: binary image"""

    #sharpened image:
    im_sharp= unsharp_mask(img_grayscale, radius=2, amount=2)

    # Equalization threshold:
    p2, p98 = np.percentile(im_sharp, (2, 98))
    im_eq = exposure.rescale_intensity(img_grayscale, in_range=(p2, p98))

    #Gaussian:
    im_gaus=gaussian_filter(im_eq, sigma=2.7)

    #Edge detection: 
    im_edge=feature.canny(im_gaus, sigma=1)

    #remove small objects:
    im_clean1 = morphology.remove_small_objects(im_edge, 200, in_place=True, connectivity=50)

    #close:
    phantom = im_clean1
    phantom[10:30, 200:210] = 0
    selem_c = disk(10)
    im_closed = closing(phantom, selem_c)

    #dialated:
    selem_d = disk(4)
    im_dialated=dilation(im_closed, selem_d)


    #remove small objects:
    im_final = morphology.remove_small_objects(im_dialated, 1700, in_place=True, connectivity=200)

    return im_final

    
if __name__ == "__main__":

    img= grayschale('image-0.tif')
    membrane=membrane_detect(img)
    plot_comparison(img, membrane, 'membrane detection')
    plt.show()