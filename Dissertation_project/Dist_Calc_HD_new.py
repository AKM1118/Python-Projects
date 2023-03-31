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
ap.add_argument("-w", "--width", type=float, required=True,
                help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (11, 11), 0)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# sort the contours from left-to-right and, then initialize the
# distance colors and reference object
(cnts, _) = contours.sort_contours(cnts)
colors = ((0, 0, 255), (0, 255, 0), (255, 0, 255), (0, 255, 255),
          (0, 0, 0))
refObj = None

# loop over the contours individually
for c in cnts:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 4500:
        continue
    # compute the rotated bounding box of the contour
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    # order the points in the contour such that they appear
    # in top-left, top-right, bottom-right, and bottom-left
    # order, then draw the outline of the rotated bounding
    # box

    box = perspective.order_points(box)
    print(box)
    # compute the center of the bounding box
    cX = np.average(box[:, 0])
    cY = np.average(box[:, 1])

    # if this is the first contour we are examining (i.e.,
    # the left-most contour), we presume this is the
    # reference object
    if refObj is None:
        # unpack the ordered bounding box, then compute the
        # midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-right and
        # bottom-right
        (tl, tr, br, bl) = box
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        # compute the Euclidean distance between the midpoints,
        # then construct the reference object
        D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        refObj = (box, (cX, cY), D / args["width"])
        x1 = int(box[0][0])
        x2 = int(box[1][0])
        y1 = int(box[0][1])
        y2 = int(box[2][1])
        continue

    cropped_img = image[y1:y2, x1:x2]
    scale_crop = 200
    width_crop = int(cropped_img.shape[1] * scale_crop / 100)
    height_crop = int(cropped_img.shape[0] * scale_crop / 100)
    dim2 = (width_crop, height_crop)
    res_crop = cv2.resize(cropped_img, dim2, interpolation=cv2.INTER_AREA)

    gray_crop = cv2.cvtColor(res_crop, cv2.COLOR_BGR2GRAY)
    gray_crop = cv2.GaussianBlur(gray_crop, (3, 3), 0)

    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edge_crop = cv2.Canny(gray_crop, 50, 100)
    edge_crop = cv2.dilate(edge_crop, None, iterations=1)
    edge_crop = cv2.erode(edge_crop, None, iterations=1)

    cnts_crop = cv2.findContours(edge_crop.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)
    cnts_crop = imutils.grab_contours(cnts_crop)

    # sort the contours from left-to-right and, then initialize the
    # distance colors and reference object
    (cnts_crop, _) = contours.sort_contours(cnts_crop)
    colors_crop = ((0, 0, 255), (0, 255, 0), (255, 0, 255), (0, 255, 255),
                   (0, 0, 0))
    refObj_crop = None
    for crop in cnts_crop:
        # if the contour is not sufficiently large, ignore it
        print("contour area is = ", cv2.contourArea(crop))
        # if cv2.contourArea(crop) > 1000 or cv2.contourArea(crop) < 10 or cv2.contourArea(crop)==416.5:
        if cv2.contourArea(crop) < 10 or cv2.contourArea(crop) == 218 or cv2.contourArea(crop) == 416.5:
            continue
        box_crop = cv2.minAreaRect(crop)
        box_crop = cv2.cv.BoxPoints(box_crop) if imutils.is_cv2() else cv2.boxPoints(box_crop)
        box_crop = np.array(box_crop, dtype="int")
        box_crop = perspective.order_points(box_crop)
        # compute the center of the bounding box
        cX_crop = np.average(box_crop[:, 0])
        cY_crop = np.average(box_crop[:, 1])

        # if this is the first contour we are examining (i.e.,
        # the left-most contour), we presume this is the
        # reference object
        if refObj_crop is None:
            # unpack the ordered bounding box, then compute the
            # midpoint between the top-left and top-right points,
            # followed by the midpoint between the top-right and
            # bottom-right
            (tl_crop, tr_crop, br_crop, bl_crop) = box_crop
            (tlblX_crop, tlblY_crop) = midpoint(tl_crop, bl_crop)
            (trbrX_crop, trbrY_crop) = midpoint(tr_crop, br_crop)
            # compute the Euclidean distance between the midpoints,
            # then construct the reference object
            D_crop = dist.euclidean((tlblX_crop, tlblY_crop), (trbrX_crop, trbrY_crop))
            refObj_crop = (box_crop, (cX_crop, cY_crop), D_crop / 4.5)

        res_orig = res_crop.copy()
        cv2.drawContours(res_orig, [box_crop.astype("int")], -1, (0, 255, 0), 2)
        cv2.drawContours(res_orig, [refObj_crop[0].astype("int")], -1, (0, 255, 0), 2)
        # stack the reference coordinates and the object coordinates
        # to include the object center
        refCoords_crop = np.vstack([refObj_crop[0], refObj_crop[1]])
        objCoords_crop = np.vstack([box_crop, (cX_crop, cY_crop)])
        # loop over the original points
        cv2.circle(res_orig, (int(box_crop[0][0]), int(box_crop[0][1])), 3, (0, 0, 0), -1)
        cv2.circle(res_orig, (int(box_crop[1][0]), int(box_crop[1][1])), 3, (0, 0, 0), -1)
        cv2.circle(res_orig, (int(box_crop[2][0]), int(box_crop[2][1])), 3, (0, 0, 0), -1)
        cv2.circle(res_orig, (int(box_crop[3][0]), int(box_crop[3][1])), 3, (0, 0, 0), -1)
        cv2.line(res_orig, (int(box_crop[0][0]), int(box_crop[0][1])), (int(box_crop[1][0]), int(box_crop[1][1])),
                 (0, 0, 255), 3)
        length1 = dist.euclidean((int(box_crop[0][0]), int(box_crop[0][1])),
                                 (int(box_crop[1][0]), int(box_crop[1][1]))) / refObj_crop[2]
        cv2.putText(res_orig, "{:.4f}cm".format(length1), (int(box_crop[0][0]), int(box_crop[0][1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
        for ((xA_crop, yA_crop), (xB_crop, yB_crop), color_crop) in zip(refCoords_crop, objCoords_crop, colors_crop):
            # draw circles corresponding to the current points and
            # connect them with a line
            cv2.circle(res_orig, (int(xA_crop), int(yA_crop)), 2, color_crop, -1)
            cv2.circle(res_orig, (int(xB_crop), int(yB_crop)), 2, color_crop, -1)
            cv2.line(res_orig, (int(xA_crop), int(yA_crop)), (int(xB_crop), int(yB_crop)),
                     color_crop, 1)

            # compute the Euclidean distance between the coordinates,
            # and then convert the distance in pixels to distance in
            # units #mX mY
            D_crop = dist.euclidean((xA_crop, yA_crop), (xB_crop, yB_crop)) / refObj_crop[2]
            (mX_crop, mY_crop) = midpoint((xA_crop, yA_crop), (xB_crop, yB_crop))
            cv2.putText(res_orig, "{:.4f}cm".format(D_crop), (int(mX_crop), int(mY_crop - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_crop, 1)
            cv2.imshow("Cropped", res_orig)
            cv2.imshow("Cropped2", edge_crop)
            cv2.waitKey(0)

    # draw the contours on the image
    orig = image.copy()
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
    cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
    # stack the reference coordinates and the object coordinates
    # to include the object center
    refCoords = np.vstack([refObj[0], refObj[1]])
    objCoords = np.vstack([box, (cX, cY)])
    # loop over the original points
    for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
        # draw circles corresponding to the current points and
        # connect them with a line
        cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
        cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
        cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
                 color, 1)
        # compute the Euclidean distance between the coordinates,
        # and then convert the distance in pixels to distance in
        # units #mX mY
        D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
        (mX, mY) = midpoint((xA, yA), (xB, yB))
        cv2.putText(orig, "{:.4f}cm".format(D), (int(mX), int(mY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 7, color, 3)
        # show the output image

        scale_percent = 15  # percent of original size
        width = int(orig.shape[1] * scale_percent / 100)
        height = int(orig.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(orig, dim, interpolation=cv2.INTER_AREA)

        width = int(orig.shape[1] * scale_percent / 100)
        height = int(orig.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resizedCanny = cv2.resize(edged, dim, interpolation=cv2.INTER_AREA)

        cv2.imshow("Image", resized)
        cv2.imshow("Binary Image", resizedCanny)
        cv2.waitKey(0)
