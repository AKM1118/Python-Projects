# program to calculate the dimensions of the marks on a photo in cm
import argparse
import cv2
import imutils
import numpy
import numpy as np
from imutils import perspective
from imutils import contours
from scipy.spatial import distance as dist
import xlwt

ret = 0.7218316116723064
mtx = [[3.52538591e+03, 0.00000000e+00, 1.64924486e+03], [0.00000000e+00, 3.55117301e+03, 1.16745770e+03],
       [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
distt = numpy.array([-2.77084427e-01, 8.14581003e-01, -1.75902601e-03, 1.31484180e-03, -2.98025019e+00], numpy.float32)
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
            if abs(x1 - x2) < 10 and y1 > y2:
                tup_list[j], tup_list[j + 1] = tup_list[j + 1], tup_list[j]
                already_sorted = False
        if already_sorted:
            break
    # check = tuple(abs(np.subtract(tup_list, key_item)))
    return tup_list
def resizeImage(img, scale):
    img_pre_resize = img.copy()
    width = int(img_pre_resize.shape[1] * scale / 100)
    height = int(img_pre_resize.shape[0] * scale / 100)
    dimensions = (width, height)
    resized_image = cv2.resize(img_pre_resize, dimensions, interpolation=cv2.INTER_AREA)
    return resized_image
def showMyImage(img, scale):
    img_show = img.copy()
    cv2.imshow("Image", resizeImage(img_show,scale))
    cv2.waitKey(0)
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
def WriteToExcel(workbook, sheetName, x_list, y_list):
    sheet1 = workbook.add_sheet(sheetName)
    for i in range(len(x_list)):
        sheet1.write(i, 0, x_list[i])
        sheet1.write(i, 5, y_list[i])
    workbook.save("point length results.xls")

workbook = xlwt.Workbook()
style = xlwt.easyxf('font: bold 1')
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

if args["contrast"] == "true":
    # Apply gamma correction
    gamma = 5.0
    # Use LookUpTable to swiftly convert image contrast by gamma value
    lookUpTable = np.empty((1, 256), np.uint8)
    for i in range(256):
        lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    new_image = cv2.LUT(image, lookUpTable)
    #showMyImage(image,30)
    #showMyImage(new_image,30)
    # Apply filtering to an image
    gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    # gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 100)
    #showMyImage(edged, 30)
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #showMyImage(gray,30)
    gray = cv2.GaussianBlur(gray, (9, 9), 0)
    #showMyImage(gray,30)
    # gray_temp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 100)
    #showMyImage(edged, 30)
    edged = cv2.dilate(edged, None, iterations=1)
    #showMyImage(edged, 30)
    edged = cv2.erode(edged, None, iterations=1)
    #showMyImage(edged, 30)
# Get all possible contours from an image
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
#showMyImage(image,10)
cnts = imutils.grab_contours(cnts)
(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
(cnts_x, _) = contours.sort_contours(cnts)
refContour = None
px_to_cm = None
length_box = []
cnts_mark = []
cntr_box_x = []
cntr_box_y = []
corners = cv2.goodFeaturesToTrack(gray, 5000, 0.1, 6)
corners = np.int0(corners)
l = 0
for c in cnts:

    # if the contour is not sufficiently large, ignore it
    #if cv2.contourArea(c) < 200:
    #    continue
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    if cv2.contourArea(box) < 2500:
        continue
    cX = np.average(box[:, 0])
    cY = np.average(box[:, 1])
    dot_box_x = []
    dot_box_y = []
    # Using a ratio to skip all non-mark contours
    ratio = ((box[0][0] - box[1][0]) ** 2 + (box[0][1] - box[1][1]) ** 2) / (
            (box[0][0] - box[3][0]) ** 2 + (box[0][1] - box[3][1]) ** 2)
    print("ratio is ", ratio)
    #if (0.10 <= ratio <= 0.45) or 0.75 <= ratio <= 1.35:
    if 0.75 <= ratio <= 1.35:
        cv2.drawContours(image, [box.astype("int")], -1, (0, 255, 0), 3)
    else:
        continue
    if refContour is None:
        refContour = box
        cnts_mark.append(box)
        for point in corners:
            outside = 0
            x, y = point.ravel()
            # skip if the point is outside the selected contour
            outside = cv2.pointPolygonTest(box, (int(x), int(y)), True)
            if outside >= 10:
                dot_box_x.append((x, y))
                dot_box_y.append((y, x))
                cv2.circle(image, (x, y), 7, (255, 0, 0), -1)
        dot_box_x = approx_sorter(dot_box_x)
        dot_box_y = approx_sorter(dot_box_y)
        cntr_box_x.append(dot_box_x)
        cntr_box_y.append(dot_box_y)
        print(f"box {l} is {cv2.contourArea(box)}")
        showMyImage(image,30)
        l+=1
        continue
    elif px_to_cm is None:
        D = dist.euclidean((refContour[1][0], refContour[1][1]), (box[0][0], box[0][1]))
        px_to_cm = D / args["width"]
        orig = image.copy()
        cv2.circle(orig, (int(refContour[1][0]), int(refContour[1][1])), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(box[0][0]), int(box[0][1])), 5, (255, 0, 0), -1)
        cv2.line(orig, (int(refContour[1][0]), int(refContour[1][1])), (int(box[0][0]), int(box[0][1])),
                 (255, 0, 0), 5)
        (mX, mY) = midpoint((refContour[0][0], refContour[0][1]), (box[0][0], box[0][1]))
        cv2.putText(orig, "{:.4f}".format(D), (int(mX), int(mY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 0, 0), 5)
        print(f"pixel per metric is {px_to_cm}")
        print(f"Pixel distance is {D}")
    cnts_mark.append(box)
    for point in corners:
        outside = 0
        x, y = point.ravel()
        # skip if the point is outside the selected contour
        outside = cv2.pointPolygonTest(box, (int(x), int(y)), True)
        if outside >= 10:
            dot_box_x.append((x, y))
            dot_box_y.append((y, x))
            cv2.circle(image, (x, y), 7, (255, 0, 0), -1)
    dot_box_x = approx_sorter(dot_box_x)
    dot_box_y = approx_sorter(dot_box_y)
    cntr_box_x.append(dot_box_x)
    cntr_box_y.append(dot_box_y)
    l += 1
    print(f"box {l} us is {cv2.contourArea(box)}")
    showMyImage(image, 30)
showMyImage(image, 30)
px = True
orig = image.copy()
#h, w = orig.shape[:2]
#newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, distt, (w, h), 1, (w, h))
#dst = cv2.undistort(orig, mtx, distt, None, newcameramtx)
borders = False
for c in cnts_mark:
    # continue
    # if px:
    #    D = dist.euclidean((c[0][0], c[0][1]), (c[1][0], c[1][1]))
    #    px_to_cm = D / args["width"]
    #    px = False
    orig = image.copy()
    i = 0
    if borders:
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
            cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
            cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
            cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),
                 color, 3)
        # compute the Euclidean distance between the coordinates,
        # and then convert the distance in pixels to distance in
        # units #mX mY
            D = dist.euclidean((xA, yA), (xB, yB)) / px_to_cm
            (mX, mY) = midpoint((xA, yA), (xB, yB))
        # cv2.putText(orig, "{:.4f}cm".format(D), (int(mX), int(mY - 10)),
        #            cv2.FONT_HERSHEY_SIMPLEX, 7, color, 3)
            cv2.putText(orig, "{:.6f}cm".format(D), (int(mX), int(mY - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 4, color, 3)
            length_box.append(D)
            i += 1
px_to_cm = 0
for cntr_num in range(len(cntr_box_x)):
    orig = image.copy()
    if len(cntr_box_x[cntr_num]) <= 15:
        continue

    prop_list_x = []
    prop_list_y = []
    dot_box_x_1 = cntr_box_x[cntr_num]
    dot_box_y_1 = cntr_box_y[cntr_num]

    orig = image.copy()
    if px_to_cm == 0:
        dot_box_x_1 = cntr_box_x[0]
        dot_box_x_2 = cntr_box_x[1]
        dot_box_y_2 = cntr_box_y[cntr_num + 1]
        D_x1 = dist.euclidean((dot_box_x_1[15][0], dot_box_x_1[15][1]), (dot_box_x_2[3][0], dot_box_x_2[3][1]))
        #D_x1 = dist.euclidean((dot_box_x_1[0][0], dot_box_x_1[0][1]), (dot_box_x_1[12][0], dot_box_x_1[12][1]))
        px_to_cm = D_x1/args["width"]
        cv2.line(orig, (int(dot_box_x_1[15][0]), int(dot_box_x_1[15][1])),
             (int(dot_box_x_2[3][0]), int(dot_box_x_2[3][1])),
             (0, 123, 255), 4)
        #cv2.line(orig, (int(dot_box_x_1[0][0]), int(dot_box_x_1[0][1])),
        #         (int(dot_box_x_1[12][0]), int(dot_box_x_1[12][1])),
        #         (0, 123, 255), 4)
        #cv2.line(orig, (int(1657), int(5)),
        #     (int(1657), int(2000)),
        #     (0, 0, 255), 4)

        (mX, mY) = midpoint((dot_box_x_1[3][0], dot_box_x_1[3][1]), (dot_box_x_2[15][0], dot_box_x_2[15][1]))
        #(mX, mY) = midpoint((dot_box_x_1[12][0], dot_box_x_1[12][1]), (dot_box_x_1[0][0], dot_box_x_1[0][1]))
        cv2.putText(orig, "{:.4f}px".format(D_x1), (int(mX), int(mY)),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (203, 192, 255), 10)
        print(f"distance is {D_x1}, metric {px_to_cm}, x1 {dot_box_x_2[3][0]},x2 {dot_box_x_1[15][0]}, y1 {dot_box_x_2[3][1]},y2 { dot_box_x_1[15][1]}, mX,mY {(mX,mY)}")
        showMyImage(orig,40)
    for i in range(len(cntr_box_x[cntr_num])-1):
        orig = image.copy()
        cv2.line(orig, (int(dot_box_x_1[i][0]), int(dot_box_x_1[i][1])),
                 (int(dot_box_x_1[i+1][0]), int(dot_box_x_1[i+1][1])),
                 (0, 0, 255), 5)
        # cv2.line(orig, (int(dot_box_x_1[j][0]), int(dot_box_x_1[j][1])),
        #         (int(dot_box_x_2[j][0]), int(dot_box_x_2[j][1])),
        #         (0, 0, 255), 2)

        cv2.line(orig, (int(dot_box_y_1[i][1]), int(dot_box_y_1[i][0])),
                 (int(dot_box_y_1[i+1][1]), int(dot_box_y_1[i+1][0])),
                 (0, 255,0), 5)
        # cv2.line(orig, (int(dot_box_y_1[j][1]), int(dot_box_y_1[j][0])),
        #         (int(dot_box_y_2[j][1]), int(dot_box_y_2[j][0])),
        #         (255, 0, 0), 2)

        # compute the Euclidean distance between the coordinates,
        # and then convert the distance in pixels to distance in
        # units #mX mY
        #D = dist.euclidean((refContour[0][0], refContour[0][1]), (refContour[1][0], refContour[1][1]))
        #px_to_cm = D / args["width"]
        #px_to_cm = 28.224190657512306 # 9 cm 1 m
        #px_to_cm = 13.610632423462906 # 123 cm 3 m
        #px_to_cm = 16.244001683180894 # 123 cm 2 m
        #px_to_cm = 16.377149237961067  122 cm 2 m
        #px_to_cm = 1.651137925480923 # 1244 mm 2 m
        #px_to_cm = 1.1809669353409809 # 1244 mm 3 m
        D_x = dist.euclidean((dot_box_x_1[i][0], dot_box_x_1[i][1]), ((dot_box_x_1[i+1][0]), dot_box_x_1[i+1][1])) / px_to_cm
        prop_list_x.append(D_x)

        cv2.putText(orig, "{:.2f}mm".format(D_x), (int(dot_box_x_1[i][0]-300), int(dot_box_x_1[i+1][1] + 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 7)
        #cv2.putText(orig, "{:.4f}deg".format(D_deg), (int(dot_box_x_1[j][0]), int(dot_box_x_1[j][1] + 30)),
        #            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 10)

        D_y = dist.euclidean((dot_box_y_1[i][1], dot_box_y_1[i][0]), ((dot_box_y_1[i+1][1]), dot_box_y_1[i+1][0])) / px_to_cm
        prop_list_y.append(D_y)

        cv2.putText(orig, "{:.2f}mm".format(D_y), (int(dot_box_y_1[i][1]), int(dot_box_y_1[i][0])-25),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 7)
        print(f"D_x is {D_x}, D_y is {D_y}")
        showMyImage(orig,30)
    WriteToExcel(workbook,f"mark {cntr_num}",prop_list_x,prop_list_y)
writer = open(f"Results/prop list {99}.txt", "w")
writer.write(f"{str(length_box)}")
writer.close()

if args["contrast"] == "True":
    image = cv2.hconcat([image, new_image])
cv2.imwrite("Results/result.jpg", image)
cv2.imwrite("Results/result_canny.jpg", edged)
