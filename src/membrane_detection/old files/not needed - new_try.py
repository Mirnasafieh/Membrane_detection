import cv2
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import scipy
from skimage.filters import unsharp_mask
import numpy as np
from PIL import Image, ImageEnhance


def edge_detection(image_inpot):

    image1 = cv2.imread(image_inpot)
    # image1 = cv2.imread("new_image.tif")
    # plt.imshow(image)

    # plt.title('Original'), plt.xticks([]), plt.yticks([])
    # plt.show()

    # im = Image.open("new_image.tif")
    # enhancer = ImageEnhance.Contrast(im)
    # factor = 3
    # im_output = enhancer.enhance(factor)
    # plt.imshow(im_output)
    # plt.title('after enhancer'), plt.xticks([]), plt.yticks([])
    # plt.show()


    image = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # gray = cv2.cvtColor(np.float32(image), cv2.COLOR_RGB2GRAY)

    # plt.imshow(gray)
    # plt.title('after greyscale'), plt.xticks([]), plt.yticks([])
    # plt.show()

    result = unsharp_mask(gray, radius=10, amount=10)
    # plt.imshow(result)
    # plt.title('after sharpen'), plt.xticks([]), plt.yticks([])
    # plt.show()
    #print(type(result))

    # plt.imshow(result, clim=(0.064, 0.068))
    # mod_img = scipy.ndimage.median_filter(result, 20)
    # plt.imshow(mod_img)
    # plt.show()
    img = cv2.GaussianBlur(result,(3,3),0)
    # plt.imshow(result)
    # plt.title('after gaussian noises'), plt.xticks([]), plt.yticks([])
    # plt.show()

    plt.subplot(2,2,1),plt.imshow(image1)
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,2),plt.imshow(gray, cmap = 'gray')
    plt.title('after grayscale'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,3),plt.imshow(result, cmap = 'gray')
    plt.title('after sharpen'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,4),plt.imshow(img, cmap = 'gray')
    plt.title('after gaussian noises'), plt.xticks([]), plt.yticks([])

    plt.show()

    # convolute with proper kernels
    laplacian = cv2.Laplacian(img,cv2.CV_64F)
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)  # x
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)  # y

    plt.subplot(2,2,1),plt.imshow(image1)
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,2),plt.imshow(laplacian, cmap = 'gray')
    plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,3),plt.imshow(sobelx, cmap = 'gray')
    plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
    plt.subplot(2,2,4),plt.imshow(sobely, cmap = 'gray')
    plt.title('Sobel Y'), plt.xticks([])

    plt.show()

    # binary = cv2.threshold(result, 225, 255, cv2.THRESH_BINARY_INV)[1]
    # print(type(binary))
    # plt.title('after binary'), plt.xticks([]), plt.yticks([])
    # plt.imshow(binary, cmap="gray")
    # plt.show()

    # contours, hierarchy = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    # plt.imshow(image)
    # plt.show()

if __name__ == "__main__":
    edge_detection("new_image.tif")