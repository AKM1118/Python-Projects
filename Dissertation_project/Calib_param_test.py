# Program created to test how different values of intrinsic camera parameters affect euler angle calculation

import numpy as np
import cv2
import glob
import math
import cam_cal


# Constants
board_x_detect = 3
board_y_detect = 7
iterations = 15

test_image = 'Dist_detect_8/SDC13146.JPG'

cam_params = np.load('cam_param.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']

fx_max_span = mtx[0][0] * 0.15
fy_max_span = mtx[1][1] * 0.15
cx_max_span = mtx[0][2] * 0.15
cy_max_span = mtx[1][2] * 0.15

fx_span = mtx[0][0] / 100
fy_span = mtx[1][1] / 100
cx_span = mtx[0][2] / 100
cy_span = mtx[1][2] / 100

print(fx_span,fy_span,cx_span,cy_span)

object_points = np.zeros((board_y_detect * board_x_detect, 3), np.float32)
object_points[:, :2] = np.mgrid[0:board_y_detect, 0:board_x_detect].T.reshape(-1, 2)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
# criteria for sub pixel corner detection
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
def main():
    img = cv2.imread(test_image)
    ret, corners, gray = cam_cal.getCorners(test_image, board_x_detect, board_y_detect)
    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    for i in range(iterations):
        ret, rvecs, tvecs = cv2.solvePnP(object_points, corners2, mtx, dist)
        # project 3D points to image plane
        imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
        xAng, yAng, zAng = cam_cal.getAngles(rvecs)
        img = cam_cal.draw(test_image, corners2, imgpts, xAng, yAng, zAng)
        cam_cal.showMyImage(img, 30)
        # showMyImage(cp, 30)
        print(mtx)
    cv2.destroyAllWindows()
"""
                        # Find the rotation and translation vectors.
            ret, rvecs, tvecs = cv2.solvePnP(object_points, corners2, mtx, dist)

            # project 3D points to image plane
            imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            xAng, yAng, zAng = getAngles(rvecs)
            img = draw(frame, corners2, imgpts, xAng, yAng, zAng)
            showMyImage(img, 30)
            # showMyImage(cp, 30)
    cv2.destroyAllWindows()
"""
if __name__ == "__main__":
    main()