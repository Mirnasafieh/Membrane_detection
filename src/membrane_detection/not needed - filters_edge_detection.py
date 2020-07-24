from skimage import data
from skimage import color
from skimage.filters import meijering, sato, frangi, hessian
import matplotlib.pyplot as plt
import skimage
from skimage.color import rgb2gray
import skimage.io
from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from numpy import asarray
from skimage import filters
from skimage.data import camera
from skimage.util import compare_images
import imagecodecs
import cv2
from skimage import data, exposure, img_as_float


def identity(image):
    # new_image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    # image_enhanced = cv2.equalizeHist(new_image)
    # greyscale = 
    # plt.imshow(image_enhanced, cmap='gray'), plt.axis("off")
    # plt.show()
    im = Image.open(image)
    # enhancer = ImageEnhance.Contrast(im)
    # factor = 3
    # im_output = enhancer.enhance(factor)
    plt.imshow(im)
    plt.show()
    original = skimage.io.imread(image)
    grayscale = rgb2gray(original)
    # plt.imshow(grayscale)
    # plt.show()
    enhanced_image = exposure.adjust_gamma(grayscale, 0.5)
    # edges = cv2.Canny(enhanced_image,100,100)

    # plt.subplot(121),plt.imshow(enhanced_image,cmap = 'gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.imshow(enhanced_image)
    plt.show()
    #plt.imshow(gamma_corrected, cmap='gray')
    #imagedata = asarray(im_output)
    # print(type(enhanced_image))
    # print(enhanced_image.shape)
    # new_img = imagedata.reshape((imagedata.shape[0]*imagedata.shape[1]), imagedata.shape[2])
    # new_img = new_img.transpose()
    # print(type(new_img))
    # print(new_img.shape)
    # plt.imshow(filters.sobel(enhanced_image))
    # plt.show()

    edge_roberts = filters.roberts(enhanced_image)
    edge_sobel = filters.sobel(enhanced_image)

    fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True, figsize=(10, 10))

    axes[0].imshow(edge_roberts, cmap=plt.cm.gray)
    axes[0].set_title('Roberts Edge Detection')

    axes[1].imshow(edge_sobel, cmap=plt.cm.gray)
    axes[1].set_title('Sobel Edge Detection')

    for ax in axes:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # im = Image.open('image-0.tif')
    # plt.imshow(im)
    # plt.show()
    identity('image-0.tif')