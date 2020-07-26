import skimage
import skimage.io
from cv2 import cv2    
from skimage.color import rgb2gray
import numpy as np
    
def membrane_detect(img_grayscale):
    """This fuction detects the membrane from a series of manipulations on a grayscale bright-field image"""
    """input: grayscale image"""
    """output: binary image"""
    # sharpened image:
    im_sharp = unsharp_mask(img_grayscale, radius=2, amount=2)
    # Equalization threshold:
    p2, p98 = np.percentile(im_sharp, (2, 98))
    im_eq = exposure.rescale_intensity(img_grayscale, in_range=(p2, p98))
    # Gaussian:
    im_gaus = gaussian_filter(im_eq, sigma=2.7)
    # Edge detection:
    im_edge = feature.canny(im_gaus, sigma=1)
    # Remove small objects:
    im_clean1 = morphology.remove_small_objects(im_edge, 200, in_place=True, connectivity=50)
    # Close:
    phantom = im_clean1
    phantom[10:30, 200:210] = 0
    selem_c = disk(10)
    im_closed = closing(phantom, selem_c)
    # Dialated:
    selem_d = disk(4)
    im_dialated = dilation(im_closed, selem_d)
    # Remove small objects:
    im_final = morphology.remove_small_objects(im_dialated, 1700, in_place=True, connectivity=200)
    return im_final




im_path='D:\DannyM19\Desktop\Membrane detection\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
img = cv2.imread(im_path)

def grayscale(img_path):
    """converts the image into a grayscale"""
    original = skimage.io.imread(img_path)
    grayscale = rgb2gray(original)
    return grayscale

img_gray=grayscale(im_path)

membrane = membrane_detect(img_gray)

print (membrane.shape)
