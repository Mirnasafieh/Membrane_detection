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
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb



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




im=grayschale('image-1.tif')
#im_roi=grayschale('new_image_2.jpg')

im2= sharpen(im)
#im2_roi= sharpen(im_roi)

im3=edge_detec(im,0.5)
#im3_roi=edge_detec(im2_roi,0.5)


plot_comparison(im2, im3, "edge detect segma 0.5 no roi")

#plot_comparison(im2_roi, im3_roi, "edge detect segma 0.5 roi")
plt.show()




""" the following code recognized subpopulations in the picture, maybe we could use it to eliminate them and clean the picture"""
#image = im

# apply threshold
thresh = threshold_otsu(image)
bw = closing(image > thresh, square(3))

# remove artifacts connected to image border
cleared = clear_border(bw)

# label image regions
label_image = label(cleared)
# to make the background transparent, pass the value of `bg_label`,
# and leave `bg_color` as `None` and `kind` as `overlay`
image_label_overlay = label2rgb(label_image, image=image, bg_label=0)

fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(image_label_overlay)

for region in regionprops(label_image):
    # take regions with large enough areas
    if region.area >= 100:
        # draw rectangle around segmented coins
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                  fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)

ax.set_axis_off()
plt.tight_layout()
plt.show()

