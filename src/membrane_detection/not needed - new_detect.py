import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from PIL import Image
from skimage.filters import unsharp_mask


def edge_det(img):
    # image_tiff = Image.open(img)
    # image_tiff.show()
    # loading image
    #img0 = cv2.imread('SanFrancisco.jpg',)
    img0 = cv2.imread(img)
    plt.imshow(img0)
    plt.show()

    # # converting to gray scale
    gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray)
    plt.show()

    # # remove noise
    nonoiseim = cv2.GaussianBlur(gray,(3,3),0)
    plt.imshow(nonoiseim)
    plt.show()

    newimg = unsharp_mask(nonoiseim, radius=5, amount=2)
    plt.imshow(newimg)
    plt.show()

    # # convolute with proper kernels
    laplacian = cv2.Laplacian(newimg,cv2.CV_64F)
    sobelx = cv2.Sobel(newimg,cv2.CV_64F,1,0,ksize=5)  # x
    sobely = cv2.Sobel(newimg,cv2.CV_64F,0,1,ksize=5)  # y

    plt.subplot(2,2,1),plt.imshow(newimg,cmap = 'gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
    plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
    plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
    plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

    # plt.imshow(img, clim=(0.064, 0.068))
    # mod_img = ndimage.median_filter(img, 20)
    # plt.imshow(mod_img)

    plt.show()

if __name__ == "__main__":
    edge_det('new_image.tif')
