# program to calculate the dimensions of the marks on a photo in cm
import argparse
import cv2
import imutils
import numpy
import numpy as np
from imutils import perspective
from imutils import contours
from scipy.spatial import distance as dist

ret = 0.7218316116723064
mtx = [[3.52538591e+03, 0.00000000e+00, 1.64924486e+03], [0.00000000e+00, 3.55117301e+03, 1.16745770e+03],
       [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
distt = numpy.array([-2.77084427e-01, 8.14581003e-01, -1.75902601e-03, 1.31484180e-03, -2.98025019e+00], numpy.float32)


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


destination = r'C:\Users\andre\Desktop\_учеба\Магистратура\диссер\Distance detection\Images'
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
ap.add_argument("-c", "--contrast", required=True,
                help="enter True if you need a gamma contrast correction")
ap.add_argument("-w", "--width", type=float, required=True,
                help="width of the left-most object in the image (in cm)")
args = vars(ap.parse_args())
# template = cv2.imread(args["template"])
image = cv2.imread(args["image"])
height, width, _ = image.shape

# image = OpenDNG(args["image"])
colors = ((0, 0, 255), (0, 255, 0), (255, 0, 255), (0, 255, 255))

if args["contrast"] == "True":
    # Apply gamma correction
    gamma = 5.0
    # Use LookUpTable to swiftly convert image contrast by gamma value
    lookUpTable = np.empty((1, 256), np.uint8)
    for i in range(256):
        lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    new_image = cv2.LUT(image, lookUpTable)
    # Apply filtering to an image
    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    # gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 100)
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 100)

# Get all possible contours from an image
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
refContour = None
px_to_cm = None
length_box = []
cnts_mark = []
for c in cnts:

    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 500:
        continue
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    cX = np.average(box[:, 0])
    cY = np.average(box[:, 1])

    # Using a ratio to skip all non-mark contours
    ratio = ((box[0][0] - box[1][0]) ** 2 + (box[0][1] - box[1][1]) ** 2) / (
            (box[0][0] - box[3][0]) ** 2 + (box[0][1] - box[3][1]) ** 2)
    #    print("ratio is ", ratio)

    # if (0.15 <= ratio <= 0.35) or 0.9 <= ratio <= 1.1:
    if 0.9 <= ratio <= 1.1:
        cv2.drawContours(image, [box.astype("int")], -1, (0, 255, 0), 3)
    else:
        continue

    if refContour is None:
        refContour = box
        cnts_mark.append(box)
        continue
    elif px_to_cm is None:
        D = dist.euclidean((refContour[0][0], refContour[0][1]), (box[0][0], box[0][1]))
        px_to_cm = D / args["width"]
        orig = image.copy()
        cv2.circle(orig, (int(refContour[0][0]), int(refContour[0][1])), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(box[0][0]), int(box[0][1])), 5, (255, 0, 0), -1)
        cv2.line(orig, (int(refContour[0][0]), int(refContour[0][1])), (int(box[0][0]), int(box[0][1])),
                 (255, 0, 0), 5)
        (mX, mY) = midpoint((refContour[0][0], refContour[0][1]), (box[0][0], box[0][1]))
        cv2.putText(orig, "{:.4f}".format(D), (int(mX), int(mY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 0, 0), 5)
        print(px_to_cm)
        width = int(orig.shape[1] * 60 / 100)
        height = int(orig.shape[0] * 60 / 100)
        dim = (width, height)
        resized = cv2.resize(orig, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Image", resized)
        cv2.waitKey(0)
    cnts_mark.append(box)
px = True
orig = image.copy()
h, w = orig.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, distt, (w, h), 1, (w, h))
dst = cv2.undistort(orig, mtx, distt, None, newcameramtx)
scale_percent = 60  # percent of original size
width = int(dst.shape[1] * scale_percent / 100)
height = int(dst.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(dst, dim, interpolation=cv2.INTER_AREA)
cv2.imshow("Image", resized)
cv2.waitKey(0)
for c in cnts_mark:
    # if px:
    #    D = dist.euclidean((c[0][0], c[0][1]), (c[1][0], c[1][1]))
    #    px_to_cm = D / args["width"]
    #    px = False
    print(c)
    orig = image.copy()
    i = 0
    for color in colors:
        if i == 3:
            xA, yA, xB, yB = c[3][0], c[3][1], c[0][0], c[0][1]
        else:
            xA, yA, xB, yB = c[i][0], c[i][1], c[i + 1][0], c[i + 1][1]
        # draw circles corresponding to the current points and
        # connect them with a line
        # cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
        ##cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
        # cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
        #         color, 3)
        cv2.circle(dst, (int(xA), int(yA)), 5, color, -1)
        cv2.circle(dst, (int(xB), int(yB)), 5, color, -1)
        cv2.line(dst, (int(xA), int(yA)), (int(xB), int(yB)),
                 color, 3)
        # compute the Euclidean distance between the coordinates,
        # and then convert the distance in pixels to distance in
        # units #mX mY
        D = dist.euclidean((xA, yA), (xB, yB)) / px_to_cm
        (mX, mY) = midpoint((xA, yA), (xB, yB))
        # cv2.putText(orig, "{:.4f}cm".format(D), (int(mX), int(mY - 10)),
        #            cv2.FONT_HERSHEY_SIMPLEX, 7, color, 3)
        cv2.putText(dst, "{:.4f}cm".format(D), (int(mX), int(mY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 7, color, 3)
        length_box.append(D)

        # scale_percent = 60    # percent of original size
        # width = int(orig.shape[1] * scale_percent / 100)
        # height = int(orig.shape[0] * scale_percent / 100)
        # dim = (width, height)
        # resized = cv2.resize(orig, dim, interpolation=cv2.INTER_AREA)
        scale_percent = 60  # percent of original size
        width = int(dst.shape[1] * scale_percent / 100)
        height = int(dst.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(dst, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("Image", resized)
        cv2.waitKey(0)
        i += 1

writer = open(f"Results/prop list {99}.txt", "w")
writer.write(f"{str(length_box)}")
writer.close()

if args["contrast"] == "True":
    image = cv2.hconcat([image, new_image])
cv2.imwrite("Results/result.jpg", image)
cv2.imwrite("Results/result_canny.jpg", edged)
