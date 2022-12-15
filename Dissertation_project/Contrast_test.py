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

alpha = 1.5
beta = -250
new_image = np.zeros(image.shape, image.dtype)
#scale_percent = 25  # percent of original size
#width = int(image.shape[1] * scale_percent / 100)
#height = int(image.shape[0] * scale_percent / 100)
#dim = (width, height)
#resized_img = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
#resized_img_new = cv2.resize(new_image, dim, interpolation=cv2.INTER_AREA)
for y in range(image.shape[0]):
	print(y, "is done")
	for x in range(image.shape[1]):
		for c in range(image.shape[2]):
			new_image[y, x, c] = np.clip(alpha*image[y, x, c]+beta, 0, 255)
		# resize image
cv2.imwrite("Contrast result.jpg",new_image)
