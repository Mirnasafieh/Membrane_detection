import matplotlib.pyplot as plt
import cv2
from skimage import data
from skimage.color import rgb2gray

def grayschale(img):
    """converts the image into a grayscale"""
    original = cv2.imread(img)
    grayscale = rgb2gray(original)

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    ax = axes.ravel()

    ax[0].imshow(original)
    ax[0].set_title("Original")
    ax[1].imshow(grayscale, cmap=plt.cm.gray)
    ax[1].set_title("Grayscale")

    fig.tight_layout()
    plt.show()
    return grayscale

print (grayschale('e3 hol 1250 1500_z0_ch02.tif'))