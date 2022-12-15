# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(args["image"])

# Gamma correction - much faster and gives a more detailed mark location
gamma = 5.0

# We create and then calculate lookup table once for 256 values
lookUpTable = np.empty((1, 256), np.uint8)
for i in range(256):
    lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

# We apply LUT to our image
new_image = cv2.LUT(image, lookUpTable)
#

# scale_percent = 25  # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)
# resized_img = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
# resized_img_new = cv2.resize(new_image, dim, interpolation=cv2.INTER_AREA)

# Old method for contrast test where we change each pixel
# Here we use alpha and beat as contrast and brightness respectively. After that we change each pixel by alpha and beta
# alpha = 1.5
# beta = -250
# new_image = np.zeros(image.shape, image.dtype)
# for y in range(image.shape[0]):
#	print(y, "is done")
#	for x in range(image.shape[1]):
#		for c in range(image.shape[2]):
#			new_image[y, x, c] = np.clip(alpha*image[y, x, c]+beta, 0, 255)
#
# resize image
cv2.imwrite("Results/Contrastik result 4.jpg", new_image)
