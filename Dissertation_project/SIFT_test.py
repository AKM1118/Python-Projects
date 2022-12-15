import argparse
import cv2
import imutils
import numpy as np
from imutils import perspective

destination = r'C:\Users\andre\Desktop\_учеба\Магистратура\диссер\Distance detection\Images'
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True,
	help="path to the input image")
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")

args = vars(ap.parse_args())
template = cv2.imread(args["template"])
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray_temp = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(image,50,100)
# SIFT implementation
#sift = cv2.SIFT_create()
#keypoints, descriptors = sift.detectAndCompute(gray,None)
#keypoints_temp, descriptors_temp = sift.detectAndCompute(gray_temp,None)
#
# ORB implementation
#orb = cv2.ORB_create(nfeatures=500)
#keypoints, descriptors = orb.detectAndCompute(gray,None)
#keypoints_temp, descriptors_temp = orb.detectAndCompute(gray_temp,None)
#image=cv2.drawKeypoints(image, keypoints,None)
#template=cv2.drawKeypoints(template, keypoints,None)

#bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
#matches = bf.match(descriptors_temp, descriptors)
#matches = sorted(matches, key = lambda x:x.distance)

#for m in matches:
#	print(m.distance)
#match_img = cv2.drawMatches(template,keypoints_temp,image,keypoints,matches[:10],None)

#Harris corner detection algorithm
dst = cv2.cornerHarris(gray_temp,2,3,0.04)
dst = cv2.dilate(dst,None)
template[dst>0.01*dst.max()]=[0,0 ,255]
#

#cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
#	cv2.CHAIN_APPROX_SIMPLE)
#cnts = imutils.grab_contours(cnts)
#(cnts, _) = contours.sort_contours(cnts)

# Good features to track test
corners = cv2.goodFeaturesToTrack(gray,550,0.05,10)
corners = np.int0(corners)
#

# visualise found contours
for c in cnts:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 4000:
        continue
    print(cv2.contourArea(c))
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    cv2.drawContours(image, [box.astype("int")], -1, (0, 255, 0), 3)


#visualise corners as edge points
for point in corners:
    #print(point)
    x,y = point.ravel()
    #print(point.ravel())
    cv2.circle(image,(x,y),4,(255,0,0),-1)
#
resize = imutils.resize(image,width = int(image.shape[1] * 0.4),height = int(image.shape[1] * 0.4))
#resize_match = imutils.resize(match_img,width = int(match_img.shape[1] * 0.3),height = int(match_img.shape[1] * 0.3))
#cv2.imwrite("result manual.jpg",image)
cv2.imshow("keypoints",resize)
#cv2.imshow("template",template)
#cv2.imshow("matching",resize_match)
cv2.waitKey(0)