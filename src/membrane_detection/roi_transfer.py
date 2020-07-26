import numpy as np
import skimage
import skimage.io
from skimage.color import rgb2gray
from skimage import feature
from skimage.filters import unsharp_mask
import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte


def grayschale(img):
    """converts the image into a grayscale"""
    original = skimage.io.imread(img)
    grayscale = rgb2gray(original)
    return grayscale


def sharpen(img):
    """sharpens the image"""
    result = unsharp_mask(img, radius=2, amount=2)
    return result


def edge_detec(img, sigma_val):
    """edge detection using skimage canny"""
    edges = feature.canny(img, sigma=sigma_val)
    return edges


def compare_images(img1, img2):
    """Returns new image with values of the fluorecent image where co-localization with membrane"""
    compare_im = np.where(img1 == False, 0, img2)
    compare_im = img_as_ubyte(compare_im)
    return (compare_im)


if __name__ == "__main__":
    original = skimage.io.imread("image-0.tif")
    gray_image = grayschale("image-0.tif")
    sharp_image = sharpen(gray_image)
    bf_im = edge_detec(sharp_image, 0.5)
    fl_im = grayschale("image-1.tif")
    new = compare_images(bf_im, fl_im)
    # print(np.argwhere(bf_im == True))
    new_im = rgb2gray(new)
    # print('bf_im', bf_im[1022,98])
    # print('fl_im', fl_im[1022,98])
    # print('new', new[1022,98])
    # print('new_im', new_im[1022,98])

    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, figsize=(8, 8))
    axes = axes.ravel()

    axes[0].imshow(original, cmap=plt.cm.gray)
    axes[0].set_title('Original image')

    axes[1].imshow(bf_im, cmap=plt.cm.gray)
    axes[1].set_title('BF image')

    axes[2].imshow(fl_im, cmap=plt.cm.gray)
    axes[2].set_title('fluorescent image')

    axes[3].imshow(new_im, cmap=plt.cm.gray)
    axes[3].set_title('comparison image')

    for ax in axes:
        ax.axis('off')

    plt.tight_layout()
    plt.show()
    # image_measurements(new)