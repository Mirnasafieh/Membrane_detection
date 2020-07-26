import skimage
import skimage.io
from cv2 import cv2    
from skimage.color import rgb2gray
import numpy as np
import pathlib



def grayscale(img_path):
    """converts the image into a grayscale"""
    original = skimage.io.imread(img_path)
    grayscale = rgb2gray(original)
    return grayscale

def compare_images(img1, img2):
    """Returns new image with values of the fluorecent image where co-localization with membrane"""
    compare_im = np.copy(img2)
    compare_im = np.where(img1 == False, 0, compare_im)
    return (compare_im)

def image_measurements(img, genotype, cell_number):
    """Returns measurements of an image"""
    total_area = img.size
    stained_area = np.count_nonzero(img)
    percent_area = (stained_area / total_area)
    total_intensity = np.sum(img)
    mean_intensity = np.mean(img)
    intigrated_optical_density = (mean_intensity * stained_area)
    return total_area, stained_area, percent_area, total_intensity, mean_intensity, intigrated_optical_density

fname = pathlib.Path('images for testing')
im1 = skimage.io.imread("D:\DannyM19\Desktop\Membrane detection\images for testing\e3 hol 1250 1500_z0_membrane.tif")
im_path="D:\DannyM19\Desktop\Membrane detection\images for testing\e3 hol 1250 1500_z0_ch02.tif"  
im2=grayscale(im_path)

print (image_measurements(im2, "E3", 1))
