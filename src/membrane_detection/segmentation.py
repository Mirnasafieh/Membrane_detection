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

def grayschale(img):
    """converts the image into a grayscale"""
    original = skimage.io.imread(img)
    grayscale = rgb2gray(original)

    return grayscale

im=grayschale('image-0.tif')
plt.imshow(im, cmap='gray')
plt.show()

def sharpen(img):
    result = unsharp_mask(im, radius=5, amount=2)
    return result

im2= sharpen(im)
plt.imshow(im2, cmap='gray')
plt.show()


def edge_detec(img):
    edges = feature.canny(img, sigma=0.4)
    return edges

im3=edge_detec(im2)
plt.imshow(im3, cmap='gray')
plt.show()

