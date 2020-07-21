from skimage.filters import sobel
from skimage.segmentation import watershed
from skimage.color import label2rgb
from scipy import ndimage as ndi
from skimage.segmentation import watershed
import numpy as np
import skimage
import skimage.io
from matplotlib import pyplot as plt
from skimage.color import rgb2gray

# a is a grayscale image 
# this function we need to manually decide the markers according to the hostgram of that image
# looking for a more effecient way


# elevation_map = sobel(a)
# fig, ax = plt.subplots(figsize=(4, 3))
# ax.imshow(elevation_map, cmap=plt.cm.gray)
# ax.set_title('elevation map')
# ax.axis('off')
# plt.show()


# from skimage.feature import canny
# edges = canny(a)
# fig, ax = plt.subplots(figsize=(4, 3))
# ax.imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
# ax.set_title('Canny detector')
# ax.axis('off')
# plt.show()

# from scipy import ndimage as ndi
# fill_holes = ndi.binary_fill_holes(edges)
# fig, ax = plt.subplots(figsize=(4, 3))
# ax.imshow(fill_holes, cmap=plt.cm.gray, interpolation='nearest')
# ax.set_title('filling the holes')
# ax.axis('off')
# #plt.show()

# #abel_objects, nb_labels = ndi.label(fill_holes)
# #sizes = np.bincount(label_objects.ravel())
# #mask_sizes = sizes > 20
# #mask_sizes[0] = 0
# #cleaned = mask_sizes[label_objects]

# im_lab, num_obj = skimage.measure.label(fill_holes, return_num=True)
# print("Number of objects found: %s" %num_obj)






# markers = np.zeros_like(a)
# markers[a < 0.1] = 1
# markers[a > 0.2] = 2



# segmentation = watershed(elevation_map, markers)
# fig, ax = plt.subplots(figsize=(4, 3))
# ax.imshow(segmentation, cmap=plt.cm.gray)
# ax.set_title('segmentation')
# ax.axis('off')
# plt.show()

# segmentation = ndi.binary_fill_holes(segmentation - 1)
# labeled_cells, _ = ndi.label(segmentation)
# image_label_overlay = label2rgb(labeled_cells, image=a, bg_label=0)

# fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
# axes[0].imshow(a, cmap=plt.cm.gray)
# axes[0].contour(segmentation, [0.5], linewidths=1.2, colors='y')
# axes[1].imshow(image_label_overlay)

# for a in axes:
#     a.axis('off')

# plt.tight_layout()

# plt.show()