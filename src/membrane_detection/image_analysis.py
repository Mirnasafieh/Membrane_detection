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

def create_hotogram(img):
    """This function creates a histogram for the image given, image should be inputed in a grayscale"""
    hist, bins = skimage.exposure.histogram(img)
    plt.plot(bins, hist, linewidth=1)
    plt.xlabel('pixel value (a.u.)')
    plt.ylabel('counts')
    plt.show()

def image_thresh(img, thresh):
    """ This function when given a picture and a threshold value, returns an image after thresholding"""
    thresh_val = thresh
    thresh_im = img > thresh_val
    plt.imshow(thresh_im, cmap='gray')
    plt.show()
    return thresh_im

def image_measurements(img,genotype,N,cell_number):
    results_dict={}

    cell_genotype=genotype
    N=N
    cell_number=cell_number
    total_area=img.size
    stained_area=np.count_nonzero(img)
    percent_area=stained_area/total_area
    total_intensity=np.sum(img)
    mean_intensity=np.mean(img)
    intigrated_optical_density=mean_intensity*stained_area #check math

    results_dict.update({"Cell genotype": cell_genotype, "N": N, "Cell number": cell_number, "total area":total_area, "stained area":stained_area, "percent area": percent_area, "total_intensity":total_intensity, "mean_intensity":mean_intensity, "intigrated_optical_density": intigrated_optical_density })
    df=pd.DataFrame.from_dict(results_dict, orient='index')
    
    return df.T

def cell_genotype(image_name):
    """returns cell genotype from the name"""
    c_name=image_name.upper()
    if (c_name.find('E3') != -1): 
        genotype="E3"
    elif (c_name.find('E4') != -1):
        genotype="E4"
    else:
        genotype="Unknown"
    
    return genotype




if __name__ == "__main__":
    image_name='e3 hol 1250 1500_z0_ch02.tif'
    a= grayschale(image_name)
    c= image_thresh(a, 0.28)
    genotype=cell_genotype(image_name)
    df1=image_measurements(c,genotype,1,1)
    df2=image_measurements(c,genotype,1,2)

    # append the results of the current measurment to the dataframe of the results
    df1=df1.append(df2)
    print (df1)