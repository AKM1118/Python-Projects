import argparse
import cv2
import imutils
import numpy
import numpy as np
from imutils import perspective
from imutils import contours
from scipy.spatial import distance as dist

import rawpy
import imageio


# Program for just finding the dots and contours on an image
# Use it if you need to test how image quality affects contour and dot search
def approx_sorter(tup_list):
    for i in range(len(tup_list)):
        already_sorted = True
        for j in range(len(tup_list) - i - 1):
            if tup_list[j] > tup_list[j + 1]:
                tup_list[j], tup_list[j + 1] = tup_list[j + 1], tup_list[j]
                already_sorted = False
        if already_sorted:
            break
    for i in range(len(tup_list)):
        already_sorted = True
        for j in range(len(tup_list) - 1):
            x1, y1 = tup_list[j]
            x2, y2 = tup_list[j + 1]
            if abs(x1 - x2) < 3 and y1 > y2:
                tup_list[j], tup_list[j + 1] = tup_list[j + 1], tup_list[j]
                already_sorted = False
        if already_sorted:
            break
    # check = tuple(abs(np.subtract(tup_list, key_item)))
    return tup_list


# Converter from RAW to png or jpeg?
def OpenDNG(path):
    with rawpy.imread(path) as raw:
        image = raw.postprocess()
    return image


destination = r'C:\Users\andre\Desktop\_учеба\Магистратура\диссер\Distance detection\Images'
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")

# Acquire template and image
args = vars(ap.parse_args())
# template = cv2.imread(args["template"])
image = cv2.imread(args["image"])
# image = OpenDNG(args["image"])

# Apply gamma correction
gamma = 5.0
lookUpTable = np.empty((1, 256), np.uint8)
for i in range(256):
    lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
new_image = cv2.LUT(image, lookUpTable)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(gray, 50, 100)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
(cnts, _) = contours.sort_contours(cnts)
(cnts_y, _) = contours.sort_contours(cnts, method="top-to-bottom")
# Good features to track test
corners = cv2.goodFeaturesToTrack(gray, 5000, 0.1, 6)
corners = np.int0(corners)
#
k = 0
cntr_box_x = []
cntr_box_y = []
# visualise found contours
for c in cnts:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 500:
        continue
    #    print(f"area is {cv2.contourArea(c)}")
    dot_box_x = []
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)

    # Using a ratio to skip all non-mark contours
    ratio = ((box[0][0] - box[1][0]) ** 2 + (box[0][1] - box[1][1]) ** 2) / (
            (box[0][0] - box[3][0]) ** 2 + (box[0][1] - box[3][1]) ** 2)
    #    print("ratio is ", ratio)
    # (0.15 <= ratio <= 0.35) or
    if 0.9 <= ratio <= 1.1:
        cv2.drawContours(image, [box.astype("int")], -1, (0, 255, 0), 3)
    else:
        continue
    # Remove all points which are outside the contour
    # Put all points in the list
    for point in corners:
        outside = 0
        x, y = point.ravel()
        # skip if the point is outside the selected contour
        outside = cv2.pointPolygonTest(c, (int(x), int(y)), True)
        if outside < 0:
            continue
        else:
            dot_box_x.append((x, y))
            cv2.circle(image, (x, y), 3, (255, 0, 0), -1)
#           print(f"point found at: {(x, y)}")
# print(f"point found: {x,y}")

image = cv2.hconcat([image, new_image])
cv2.imwrite("Results/result.jpg", image)
