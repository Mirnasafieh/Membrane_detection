import skimage
import skimage.io
from cv2 import cv2    
from skimage.color import rgb2gray
import numpy as np
    
def grayscale(img_path):
    """converts the image into a grayscale"""
    original = skimage.io.imread(img_path)
    grayscale = rgb2gray(original)
    return grayscale




im_path='D:\DannyM19\Desktop\Membrane detection\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
img = cv2.imread(im_path)

print (np.count_nonzero(img))
img_gray=grayscale(im_path)

print  (np.count_nonzero(img_gray))