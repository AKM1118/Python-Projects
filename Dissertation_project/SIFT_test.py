# Obsolete module for SIFT, ORB functionality testing
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
            x2, y2 = tup_list[j+1]
            if abs(x1-x2) < 3 and y1 > y2:
                tup_list[j], tup_list[j + 1] = tup_list[j + 1], tup_list[j]
                already_sorted = False
        if already_sorted:
            break
    #check = tuple(abs(np.subtract(tup_list, key_item)))
    return tup_list

# Converter from RAW to png or jpeg?
def OpenDNG(path):
    with rawpy.imread(path) as raw:
        image = raw.postprocess()
    return image
destination = r'C:\Users\andre\Desktop\_учеба\Магистратура\диссер\Distance detection\Images'
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-t", "--template", required=True,
#                help="path to the input image")
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")

# Acquire template and image
args = vars(ap.parse_args())
#template = cv2.imread(args["template"])
image = cv2.imread(args["image"])
#image = OpenDNG(args["image"])

# Apply gamma correction
gamma = 5.0
lookUpTable = np.empty((1, 256), np.uint8)
for i in range(256):
    lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
new_image = cv2.LUT(image, lookUpTable)
gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
#gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 50, 100)

# SIFT implementation
# sift = cv2.SIFT_create()
# keypoints, descriptors = sift.detectAndCompute(gray,None)
# keypoints_temp, descriptors_temp = sift.detectAndCompute(gray_temp,None)
#
# ORB implementation
# orb = cv2.ORB_create(nfeatures=500)
# keypoints, descriptors = orb.detectAndCompute(gray,None)
# keypoints_temp, descriptors_temp = orb.detectAndCompute(gray_temp,None)
# image=cv2.drawKeypoints(image, keypoints,None)
# template=cv2.drawKeypoints(template, keypoints,None)

# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
# matches = bf.match(descriptors_temp, descriptors)
# matches = sorted(matches, key = lambda x:x.distance)

# for m in matches:
#	print(m.distance)
# match_img = cv2.drawMatches(template,keypoints_temp,image,keypoints,matches[:10],None)

# Harris corner detection algorithm
# dst = cv2.cornerHarris(gray_temp,2,3,0.04)
# dst = cv2.dilate(dst,None)
# template[dst>0.01*dst.max()]=[0,0 ,255]
#

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
(cnts, _) = contours.sort_contours(cnts)

# Good features to track test
corners = cv2.goodFeaturesToTrack(gray, 5000, 0.1, 6)
corners = np.int0(corners)
#
k = 0
# visualise found contours
for c in cnts:

    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 500:
        continue
    print(f"area is {cv2.contourArea(c)}")
    dot_box_x = []
    dot_box_y = dot_box_x.copy()
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)

    # Using a ratio to skip all non-mark contours
    ratio = ((box[0][0] - box[1][0]) ** 2 + (box[0][1] - box[1][1]) ** 2) / (
                (box[0][0] - box[3][0]) ** 2 + (box[0][1] - box[3][1]) ** 2)
    print("ratio is ", ratio)
    if (0.15 <= ratio <= 0.35) or (0.9 <= ratio <= 1.1):
        cv2.drawContours(image, [box.astype("int")], -1, (0, 255, 0), 3)
    else:
        continue
    for point in corners:
        i = 0
        outside = 0
        x, y = point.ravel()
        # skip if the point is outside the selected contour
        outside = cv2.pointPolygonTest(c, (int(x), int(y)), True)
        if outside < 0:
            continue
        else:
            dot_box_x.append((x, y))
            dot_box_y.append((y, x))
            cv2.circle(image, (x, y), 3, (255, 0, 0), -1)
            print(f"point found at: {(x,y)}")
            #print(f"point found: {x,y}")
            i += 1
    dot_box_x = approx_sorter(dot_box_x)
    dot_box_y = approx_sorter(dot_box_y)
    print("dot box before is ", dot_box_x)
    for i in box:
        x1, y1 = i
        for j in dot_box_x:
            x2, y2 = j
            #print(f"{x1} - {x2} = {x1 - x2} , {y1} - {y2} = {y1 - y2}")
            if abs(int(x1) - int(x2)) <= 3 and abs(int(y1) - int(y2)) <= 3:
                dot_box_x.remove(j)
                #print("point above is removed")
                break
        for j in dot_box_y:
            y2, x2 = j
            #print(f"{x1} - {x2} = {x1 - x2} , {y1} - {y2} = {y1 - y2}")
            if abs(int(x1) - int(x2)) <= 3 and abs(int(y1) - int(y2)) <= 3:
                dot_box_y.remove(j)
                #print("point above is removed")
                break
    print(cv2.contourArea(c))
    #print("test tuple x variable is:", dot_box_x[0][0])
    #print("test tuple y variable is:", dot_box_x[0][1])
    print("box value is ", box)
    print("dot box is ", dot_box_x)
    print("_________")
    i = 0

    D_x = dist.euclidean((int(dot_box_x[0][0]), int(dot_box_x[0][1])), (int(dot_box_x[1][0]), int(dot_box_x[1][1])))
    D_y = dist.euclidean((int(dot_box_y[0][0]), int(dot_box_y[0][1])), (int(dot_box_y[1][0]), int(dot_box_y[1][1])))
    prop_list_x = []
    prop_list_y = prop_list_x.copy()
    prop_list_deg_x = prop_list_x.copy()
    prop_list_deg_y = prop_list_x.copy()
    while i < int(len(dot_box_x))-1:
        orig = image.copy()
        # draw circles corresponding to the current points and
        # connect them with a line
        cv2.line(orig, (int(dot_box_x[i][0]), int(dot_box_x[i][1])), (int(dot_box_x[i+1][0]), int(dot_box_x[i+1][1])),
                 (203, 192, 255), 2)
        cv2.line(orig, (int(dot_box_x[i][0]), int(dot_box_x[i][1])),
                 (int(dot_box_x[i][0]), int(dot_box_x[i + 1][1])),
                 (0, 0, 255), 2)
        # compute the Euclidean distance between the coordinates,
        # and then convert the distance in pixels to distance in
        # units #mX mY
        D = dist.euclidean((dot_box_x[i][0], dot_box_x[i][1]), ((dot_box_x[i+1][0]), dot_box_x[i+1][1]))
        D_arccos = dist.euclidean((dot_box_x[i][0], dot_box_x[i][1]), ((dot_box_x[i][0]), dot_box_x[i+1][1]))
        if dot_box_x[i][0] - dot_box_x[i + 1][0] <= 0:
            D_deg = -numpy.arccos(D_arccos / D)
        else:
            D_deg = numpy.arccos(D_arccos / D)
        prop_list_x.append(D/D_x)
        prop_list_deg_x.append(D_deg)
        cv2.putText(orig, "{:.4f}px".format(D), (int(dot_box_x[i][0]), int(dot_box_x[i][1] + 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (203, 192, 255), 2)
        cv2.putText(orig, "{:.4f}deg".format(D_deg), (int(dot_box_x[i][0]), int(dot_box_x[i][1] + 30)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
        # show the output image
        orig2 = image.copy()
        # draw circles corresponding to the current points and
        # connect them with a line
        cv2.line(orig2, (int(dot_box_y[i][1]), int(dot_box_y[i][0])),
                 (int(dot_box_y[i + 1][1]), int(dot_box_y[i + 1][0])),
                 (203, 192, 255), 2)
        cv2.line(orig2, (int(dot_box_y[i][1]), int(dot_box_y[i][0])),
                 (int(dot_box_y[i + 1][1]), int(dot_box_y[i][0])),
                 (0, 0, 255), 2)
        # compute the Euclidean distance between the coordinates,
        # and then convert the distance in pixels to distance in
        # units #mX mY
        D = dist.euclidean((dot_box_y[i][1], dot_box_y[i][0]), ((dot_box_y[i + 1][1]), dot_box_y[i + 1][0]))
        D_arccos = dist.euclidean((dot_box_y[i][0], dot_box_y[i][1]), ((dot_box_y[i][0]), dot_box_y[i + 1][1]))
        if dot_box_y[i][0] - dot_box_y[i + 1][0] >= 0:
            D_deg = -numpy.arccos(D_arccos / D)
        else:
            D_deg = numpy.arccos(D_arccos / D)
        prop_list_y.append(D / D_y)
        prop_list_deg_y.append(D_deg)
        cv2.putText(orig2, "{:.4f}px".format(D), (int(dot_box_y[i][1]) + 10, int(dot_box_y[i][0])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (203, 192, 255), 2)
        cv2.putText(orig2, "{:.4f}deg".format(D_deg),
                    (int(dot_box_y[i][1]), int(dot_box_y[i][0] + 30)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
        # show the output image
        i += 1
        orig = cv2.hconcat([orig, orig2])
        cv2.imshow("Image", orig)
        cv2.waitKey(0)
# visualise corners as edge points
    writer = open(f"Results/prop list {k}.txt", "w")
    writer.write(f"{str(prop_list_x)}\n\n{str(prop_list_y)}\n\n{str(prop_list_deg_x)}\n\n{str(prop_list_deg_y)}")
    writer.close()
    k += 1
#
image = cv2.hconcat([image, new_image])
# resize = imutils.resize(image,width = int(image.shape[1] * 0.4),height = int(image.shape[1] * 0.4))
# resize_match = imutils.resize(match_img,width = int(match_img.shape[1] * 0.3),height = int(match_img.shape[1] * 0.3))
cv2.imwrite("Results/result.jpg", image)
# cv2.imshow("keypoints",resize)
# cv2.imshow("template",template)
# cv2.imshow("matching",resize_match)
# cv2.waitKey(0)
