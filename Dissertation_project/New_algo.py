# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import glob


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True,
	help="path to the template image")
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
#ap.add_argument("-w", "--width", type=float, required=True,
#	help="width of the left-most object in the image (in cm)")
ap.add_argument("-v", "--visualize",
	help="Flag indicating whether or not to visualize each iteration")
args = vars(ap.parse_args())


# load the template
template = cv2.imread(args["template"])
resized_temp = imutils.resize(template, width = int(template.shape[1] * 0.05))
resized_temp = cv2.cvtColor(resized_temp, cv2.COLOR_BGR2GRAY)
edged_temp = cv2.Canny(resized_temp, 50, 100)
(tH, tW) = resized_temp.shape[:2]
# load the image

image = cv2.imread(args["image"])

alpha = 1.5     # Contrast
beta = -250     # Brightness

# Create a new zero matrix for image modification
#new_image = np.zeros(image.shape, image.dtype)

# Resizer to scale down the image (makes the algo work faster if used
#scale_percent = 25  # percent of original size
#width = int(image.shape[1] * scale_percent / 100)
#height = int(image.shape[0] * scale_percent / 100)
#dim = (width, height)
#resized_img = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
#resized_img_new = cv2.resize(new_image, dim, interpolation=cv2.INTER_AREA)

# Change every pixel contrast and brightness value by a fixed amount
#for y in range(resized_img.shape[0]):
#	print(y, "is done")
#	for x in range(resized_img.shape[1]):
#		for c in range(resized_img.shape[2]):
#			resized_img_new[y, x, c] = np.clip(alpha*resized_img[y, x, c]+beta, 0, 255)
# Show the modified image and compare it with the original
#cv2.imshow("Image",resized_img)
#cv2.imshow("New Image", resized_img_new)
#cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)

found = None
cv2.imshow("Template", resized_temp)
# loop over the scales of the image
for scale in np.linspace(0.3, 1.0, 20)[::-1]:
	# resize the image according to the scale, and keep track
	# of the ratio of the resizing
	resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
	r = gray.shape[1] / float(resized.shape[1])
	# if the resized image is smaller than the template, then break
	# from the loop
	if resized.shape[0] < tH or resized.shape[1] < tW:
		break
	# detect edges in the resized, grayscale image and apply template
	# matching to find the template in the image
	edged = cv2.Canny(resized, 50, 200)
	result = cv2.matchTemplate(edged, resized_temp, cv2.TM_CCOEFF_NORMED)
	(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
	# check to see if the iteration should be visualized
	if args.get("visualize", False):
		# draw a bounding box around the detected region
		clone = np.dstack([edged, edged, edged])
		cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
					  (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
		cv2.imshow("Visualize", clone)
		cv2.waitKey(0)
	# if we have found a new maximum correlation value, then update
	# the bookkeeping variable
	print("Max Corr val =",maxVal)
	if found is None or maxVal > found[0]:
		found = (maxVal, maxLoc, r)
# unpack the bookkeeping variable and compute the (x, y) coordinates
# of the bounding box based on the resized ratio
(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
# draw a bounding box around the detected result and display the image
cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
cv2.imwrite("Image for template.jpg", image)
cv2.waitKey(0)