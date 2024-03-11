# Obsolete module for distance calculation inside the marks based on corner points
import argparse
import cv2
import imutils
import numpy
import numpy as np
from imutils import perspective
from imutils import contours
from scipy.spatial import distance as dist

#import rawpy
#import imageio
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
# Does approximate sorting for dots in the contour
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
            if abs(x1 - x2) < 6 and y1 > y2:
                tup_list[j], tup_list[j + 1] = tup_list[j + 1], tup_list[j]
                already_sorted = False
        if already_sorted:
            break
    # check = tuple(abs(np.subtract(tup_list, key_item)))
    return tup_list


# Converter from RAW to png or jpeg?
#def OpenDNG(path):
#    with rawpy.imread(path) as raw:
#        image = raw.postprocess()
#    return image


destination = r'C:\Users\andre\Desktop\_учеба\Магистратура\диссер\Distance detection\Images'
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
ap.add_argument("-c", "--contrast", required=True,
                help="enter True if you need a gamma contrast correction")
ap.add_argument("-d", "--distance", required=True,
                help="enter True if you want to calculate distance between dots")
# Acquire template and image
args = vars(ap.parse_args())
# template = cv2.imread(args["template"])
image = cv2.imread(args["image"])
# image = OpenDNG(args["image"])

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
    edged = cv2.GaussianBlur(gray, (11,11), 0)
    edged = cv2.Canny(gray, 50, 100)
    #edged = cv2.dilate(edged, None, iterations=2)
    #edged = cv2.erode(edged, None, iterations=2)
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 100)

# Get all possible contours from an image
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
refObj = None
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
    cX = np.average(box[:, 0])
    cY = np.average(box[:, 1])


    # Using a ratio to skip all non-mark contours
    ratio = ((box[0][0] - box[1][0]) ** 2 + (box[0][1] - box[1][1]) ** 2) / (
            (box[0][0] - box[3][0]) ** 2 + (box[0][1] - box[3][1]) ** 2)
    #    print("ratio is ", ratio)
    #
    if (0.15 <= ratio <= 0.35) or 0.9 <= ratio <= 1.1:
        cv2.drawContours(image, [box.astype("int")], -1, (0, 255, 0), 3)
    else:
        continue
    # Remove all points which are outside the contour
    # Put all points in the list
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
            cv2.circle(image, (x, y), 6, (255, 0, 0), -1)
            #           print(f"point found at: {(x, y)}")
            # print(f"point found: {x,y}")
            i += 1

    dot_box_x = approx_sorter(dot_box_x)
    #    print("dot box before is ", dot_box_x)
    # Remove all points on the contour
    for i in box:
        x1, y1 = i
        for j in dot_box_x:
            x2, y2 = j
            #            print(f"{x1} - {x2} = {x1 - x2} , {y1} - {y2} = {y1 - y2}")
            if abs(int(x1) - int(x2)) <= 6 and abs(int(y1) - int(y2)) <= 6:
                dot_box_x.remove(j)
                #                print("point above is removed")
                break
    if len(dot_box_x) < 12:
        continue
    else:
        cntr_box_x.append(dot_box_x)

    #    print(cv2.contourArea(c))
    # print("test tuple x variable is:", dot_box_x[0][0])
    # print("test tuple y variable is:", dot_box_x[0][1])
    #    print("box value is ", box)
    #    print("dot box is ", dot_box_x)
    print("_________")
    i = 0
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
        refObj = (box, (cX, cY), D / 10)
        continue
for c in cnts_y:
    if cv2.contourArea(c) < 500:
        continue
    #    print(f"area is {cv2.contourArea(c)}")
    dot_box_y = []

    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)

    ratio = ((box[0][0] - box[1][0]) ** 2 + (box[0][1] - box[1][1]) ** 2) / (
            (box[0][0] - box[3][0]) ** 2 + (box[0][1] - box[3][1]) ** 2)
    #    print("ratio is ", ratio)
    if not (0.9 <= ratio <= 1.1):
        continue
    # Remove all points which are outside the contour
    # Put all points in the list
    for point in corners:
        i = 0
        outside = 0
        x, y = point.ravel()
        # skip if the point is outside the selected contour
        outside = cv2.pointPolygonTest(c, (int(x), int(y)), True)
        if outside < 0:
            continue
        else:
            dot_box_y.append((y, x))
            #            print(f"point found at: {(x, y)}")
            # print(f"point found: {x,y}")
            i += 1
    dot_box_y = approx_sorter(dot_box_y)
    for i in box:
        x1, y1 = i
        for j in dot_box_y:
            x2, y2 = j
            print(f"{y1} - {x2} = {y1 - x2} , {x1} - {y2} = {x1 - y2}")
            if abs(int(y1) - int(x2)) <= 6 and abs(int(x1) - int(y2)) <= 6:
                dot_box_y.remove(j)
                print("point above is removed")
                break
    if len(dot_box_y) < 12:
        continue
    else:
        cntr_box_y.append(dot_box_y)
print(cntr_box_x)
if args["distance"] == "True":
    dot_box_x_1 = cntr_box_x[0]
    dot_box_x_2 = cntr_box_x[1]
    D_x = dist.euclidean((int(dot_box_x_1[0][0]), int(dot_box_x_1[0][1])), (int(dot_box_x_2[0][0]), int(dot_box_x_2[0][1])))
    D_x_cm = D_x / 81.5

    dot_box_y_1 = cntr_box_y[0]
    dot_box_y_2 = cntr_box_y[1]
    D_y = dist.euclidean((int(dot_box_y_1[0][0]), int(dot_box_y_1[0][1])), (int(dot_box_y_2[0][0]), int(dot_box_y_2[0][1])))
    D_y_cm = D_y / 288
    for i in range(len(cntr_box_x) - 1):

        dot_box_x_1 = cntr_box_x[i]
        dot_box_x_2 = cntr_box_x[i + 1]

        dot_box_y_1 = cntr_box_y[i]
        dot_box_y_2 = cntr_box_y[i + 1]

        prop_list_x = []
        prop_list_deg_x = prop_list_x.copy()

        prop_list_y = []
        prop_list_deg_y = prop_list_y.copy()

        for j in range(int(len(dot_box_x_1))):
            orig = image.copy()
            # draw circles corresponding to the current points and
            # connect them with a line
            #cv2.line(orig, (int(dot_box_x_1[j][0]), int(dot_box_x_1[j][1])),
            #     (int(dot_box_x_2[j][0]), int(dot_box_x_2[j][1])),
            #     (203, 192, 255), 4)
        #cv2.line(orig, (int(dot_box_x_1[j][0]), int(dot_box_x_1[j][1])),
        #         (int(dot_box_x_2[j][0]), int(dot_box_x_2[j][1])),
        #         (0, 0, 255), 2)

            cv2.line(orig, (int(dot_box_y_1[j][1]), int(dot_box_y_1[j][0])),
                 (int(dot_box_y_2[j][1]), int(dot_box_y_2[j][0])),
                 (255, 165, 0), 4)
        #cv2.line(orig, (int(dot_box_y_1[j][1]), int(dot_box_y_1[j][0])),
        #         (int(dot_box_y_2[j][1]), int(dot_box_y_2[j][0])),
        #         (255, 0, 0), 2)

        # compute the Euclidean distance between the coordinates,
        # and then convert the distance in pixels to distance in
        # units #mX mY
            D = dist.euclidean((dot_box_x_1[j][0], dot_box_x_1[j][1]), ((dot_box_x_2[j][0]), dot_box_x_2[j][1])) / refObj[2]
            D_arccos = dist.euclidean((dot_box_x_1[j][0], dot_box_x_1[j][1]), ((dot_box_x_1[j][0]), dot_box_x_2[j][1]))
            if dot_box_x_1[j][0] - dot_box_x_2[j][0] <= 0:
                D_deg = -numpy.arccos(D_arccos / D)
            else:
                D_deg = numpy.arccos(D_arccos / D)
            prop_list_x.append(D)
            prop_list_deg_x.append(D_deg)

            #cv2.putText(orig, "{:.4f}cm".format(D), (int(dot_box_x_1[j][0]), int(dot_box_x_2[j][1] + 10)),
            #        cv2.FONT_HERSHEY_SIMPLEX, 3, (203, 192, 255), 10)
        #cv2.putText(orig, "{:.4f}deg".format(D_deg), (int(dot_box_x_1[j][0]), int(dot_box_x_1[j][1] + 30)),
        #            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 10)

            D = dist.euclidean((dot_box_y_1[j][1], dot_box_y_1[j][0]), ((dot_box_y_2[j][1]), dot_box_y_2[j][0])) / refObj[2]
            D_arccos = dist.euclidean((dot_box_y_1[j][0], dot_box_y_1[j][1]), ((dot_box_y_1[j][0]), dot_box_y_2[j][1]))
            if dot_box_y_1[j][0] - dot_box_y_2[j][0] <= 0:
                D_deg = -numpy.arccos(D_arccos / D)
            else:
                D_deg = numpy.arccos(D_arccos / D)
            prop_list_y.append(D)
            prop_list_deg_y.append(D_deg)

            cv2.putText(orig, "{:.4f}cm".format(D), (int((dot_box_y_1[j][0]+dot_box_y_2[j][0])*0.5), int((dot_box_y_1[j][0]+dot_box_y_2[j][0])*0.5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 156, 0), 10)
        # cv2.putText(orig, "{:.4f}deg".format(D_deg), (int(dot_box_y_1[j][1]), int(dot_box_y_1[j][0] + 30)),
        #            cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
        # show the output image

            scale_percent = 25  # percent of original size
            width = int(orig.shape[1] * scale_percent / 100)
            height = int(orig.shape[0] * scale_percent / 100)
            dim = (width, height)

            # resize image
            resized = cv2.resize(orig, dim, interpolation=cv2.INTER_AREA)

            cv2.imshow("Image", resized)
            cv2.waitKey(0)

        # visualise corners as edge points
        writer = open(f"Results/prop list {k}.txt", "w")
        writer.write(f"{str(prop_list_x)}\n\n{str(prop_list_y)}\n\n{str(prop_list_deg_x)}\n\n{str(prop_list_deg_y)}")
        writer.close()
        k += 1
#   part for distance calculation differences between

if args["contrast"] == "True":
    image = cv2.hconcat([image, new_image])
#    image = cv2.vconcat([image, edged])
# resize = imutils.resize(image,width = int(image.shape[1] * 0.4),height = int(image.shape[1] * 0.4))
# resize_match = imutils.resize(match_img,width = int(match_img.shape[1] * 0.3),height = int(match_img.shape[1] * 0.3))
cv2.imwrite("Results/result.jpg", image)
cv2.imwrite("Results/result2.jpg", edged)

# cv2.imshow("keypoints",resize)
# cv2.imshow("template",template)
# cv2.imshow("matching",resize_match)
# cv2.waitKey(0)
