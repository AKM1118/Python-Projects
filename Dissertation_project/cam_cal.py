# module for camera calibration before the main algorithm
import numpy
import numpy as np
import cv2
import glob
# criteria for sub pixel corner detection
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# creating arrays to store all found corner points
object_points = np.zeros((6*9, 3), np.float32)
object_points[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
# arrays where we store points from processed images
points_on_object = []
points_on_image = []
# find all images used for calibration
images = glob.glob('*.jpeg')
# perform corner point extraction for every image found in the folder
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCornersSB(gray, (9, 6), None)
    if ret:
        points_on_object.append(object_points)
        corners_sub_pixel = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        points_on_image.append(corners_sub_pixel)
        cv2.drawChessboardCorners(img, (9, 6), corners_sub_pixel, ret)

    scale_percent = 40  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('img', resized)
    cv2.waitKey(0)
cv2.destroyAllWindows()
# extracting calibration parameters from calibration images
ret,mtx,dist,rvecs,tvecs = cv2.calibrateCamera(points_on_object,points_on_image, gray.shape[::-1], None, None)
print(ret,mtx,dist,rvecs,tvecs)

# using said parameters to undistort an unrelated image
img = cv2.imread('20230806_174053.jpeg')
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
#image = cv2.hconcat([img, dst])
cv2.imwrite('calibresult1.png', img)
cv2.imwrite('calibresult2.png', dst)