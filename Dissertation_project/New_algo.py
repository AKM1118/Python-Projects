# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import glob
import threading

Template1 = cv2.imread(".\\Images\\template_1.jpg", 0)
Template2 = cv2.imread(".\\Images\\template_2.jpg", 0)
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-t", "--template", required=True,
                help="path to the template image")
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
ap.add_argument("-v", "--visualize",
                help="Flag indicating whether or not to visualize each iteration")
args = vars(ap.parse_args())


def processFrameConcurrent(idx, frame, template, rlist):
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    rlist.append((idx, cv2.minMaxLoc(res)))


def GetSignThread(image):
	grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	c = 0
	curMaxVal = 0
	curMaxTemplate = -1
	curMaxLoc = (0, 0)
	ThreadList = []
	ReturnList = []
	for template in AllSigns:
		t = threading.Thread(target=processFrameConcurrent, args=(c, grey, template, ReturnList))
		t.daemon = True
		t.start()
		ThreadList.append(t)
		c = c + 1
	# Wait for each thread to finish
	for th in ThreadList:
		th.join()
	# process the returns
	for (idx, (min_val, max_val, min_loc, max_loc)) in ReturnList:
		if max_val > TemplateThreshold and max_val > curMaxVal:
			curMaxVal = max_val
			curMaxTemplate = idx
			curMaxLoc = max_loc

	if curMaxTemplate == -1:
		return (-1, (0, 0), 0, 0)
	else:
		return (curMaxTemplate % 3, curMaxLoc, 1 - int(curMaxTemplate / 3) * 0.2, curMaxVal)


def GetSignSingle(image):
	grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	c = 0
	curMaxVal = 0
	curMaxTemplate = -1
	curMaxLoc = (0, 0)
	for template in AllSigns:
		res = cv2.matchTemplate(grey, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		if max_val > TemplateThreshold and max_val > curMaxVal:
			curMaxVal = max_val
			curMaxTemplate = c
			curMaxLoc = max_loc
		c = c + 1
	if curMaxTemplate == -1:
		return (-1, (0, 0), 0, 0)
	else:
		return (curMaxTemplate % 3, curMaxLoc, 1 - int(curMaxTemplate / 3) * 0.2, curMaxVal)

Templates = [Template1, Template2]
AllSigns = []
for scint in range(100, 10, -10):
    scale = scint / 100.0
    for stemp in Templates:
        AllSigns.append(cv2.resize(stemp, (int(64 * scale), int(64 * scale))))

TemplateToString = {0: "template_1", 1: "template_2"}
TemplateThreshold = 0.25

# load the template
# template = cv2.imread(args["template"])
# gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# edged_temp = cv2.Canny(gray_temp, 50, 100)
# temp_resized = imutils.resize(gray_temp, width = int(gray_temp.shape[1] * 0.15))
# (tH, tW) = temp_resized.shape[:2]
# load the image

image = cv2.imread(args["image"])
gamma = 5.0

# We create and then calculate lookup table once for 256 values
lookUpTable = np.empty((1, 256), np.uint8)
for i in range(256):
    lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

# We apply LUT to our image
new_image = cv2.LUT(image, lookUpTable)
gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 50, 100)
#found = None
# loop over the scales of the image
template = -1
(template, top_left, scale, val) = GetSignSingle(image)
if template != -1:
        bottom_right = (top_left[0] + int(64*scale), top_left[1] + int(64*scale))
        cv2.rectangle(image,top_left, bottom_right, 255, 5)
        cv2.putText(image,str(val),(20,300),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)
        cv2.putText(image,TemplateToString[template],(20,400),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),2)
cv2.imwrite("Results/Image for template.jpg", image)
cv2.waitKey(0)
