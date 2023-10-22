# module for camera calibration before the main algorithm
import numpy as np
import cv2
import glob
import math
def draw(img, corners, imgpts, xAng, yAng, zAng):
 corner = tuple(corners[0].ravel())
 imgx = tuple(imgpts[0].ravel())
 imgy = tuple(imgpts[1].ravel())
 imgz = tuple(imgpts[2].ravel())
 print(corner)
 print(tuple(imgpts[0].ravel()))
 img = cv2.line(img, (int(corner[0]),int(corner[1])), (int(imgx[0]),int(imgx[1])), (255,0,0), 5)
 img = cv2.line(img, (int(corner[0]),int(corner[1])), (int(imgy[0]),int(imgy[1])), (0,255,0), 5)
 img = cv2.line(img, (int(corner[0]),int(corner[1])), (int(imgz[0]),int(imgz[1])), (0,0,255), 5)
 cv2.putText(img, "xAng {:.4f}".format(xAng), ((int(imgx[0]),int(imgx[1]-10))),
             cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 0, 0), 5)
 cv2.putText(img, "yAng {:.4f}".format(yAng), ((int(imgy[0]),int(imgy[1]-10))),
             cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 255, 0), 5)
 #cv2.putText(img, "zAng {:.4f}".format(zAng), ((int(imgz[0]),int(imgz[1]-10))),
 #            cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 0, 255), 5)
 return img

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
a = None
a = np.load('cam_param.npz')
mtx= a['mtx']
dist = a['dist']
print(f"mtx = {mtx} # "
      f"dist = {dist} # ")
# criteria for sub pixel corner detection
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# creating arrays to store all found corner points
object_points = np.zeros((6*9, 3), np.float32)
object_points[:, :2] = np.mgrid[0:6, 0:9].T.reshape(-1, 2)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
# arrays where we store points from processed images
points_on_object = []
points_on_image = []
# find all images used for calibration
images = glob.glob('*.jpg')
image_test = glob.glob('test_image/*.JPG')
# perform corner point extraction for every image found in the folder
if a is None:
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (6, 9), None)
        if ret:
            points_on_object.append(object_points)
            corners_sub_pixel = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            points_on_image.append(corners_sub_pixel)
            cv2.drawChessboardCorners(img, (6, 9), corners, ret)
            for i in range(len(corners_sub_pixel)):
                coord = corners_sub_pixel[i]
                x = coord[0,0]
                y = coord[0,1]
                #cv2.circle(img, (int(x), int(y)), 8, (175+i,39+i, 45+i), -1)
                #cv2.putText(img, "{}".format(i),
                #            (int(x - 50), int(y - 20)), cv2.FONT_HERSHEY_SIMPLEX,
                #            0.8, (175+i, 39+i, 45+i), 2)
            #for i in range(len(corners_sub_pixel)):
            #    y = (corners_sub_pixel[i,0]-corners_sub_pixel[i,0])
            #for i in range(len(corners_sub_pixel) / 6):
            #    x = (corners_sub_pixel[i, 0] - corners_sub_pixel[i, 0])

        #scale_percent = 55  # percent of original size
        #width = int(img.shape[1] * scale_percent / 100)
        #height = int(img.shape[0] * scale_percent / 100)
        #dim = (width, height)
        #resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        #cv2.imshow('img', resized)
        #cv2.waitKey(0)
    #cv2.destroyAllWindows()
# extracting calibration parameters from calibration images
    ret,mtx,dist,rvecs,tvecs = cv2.calibrateCamera(points_on_object,points_on_image, gray.shape[::-1], None, None)
    np.savez('cam_param', mtx=mtx, dist=dist)
    print(f"mtx = {mtx} # "
      f"dist = {dist} # ")
    #################################################################
    # using said parameters to undistort an unrelated image
    img = cv2.imread('SDC12902.JPeG')
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    cv2.imwrite('calibresult2.png', dst)
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    cv2.imwrite('calibresult3.png', dst)
# crop the image
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
# image = cv2.hconcat([img, dst])
    cv2.imwrite('calibresult1.png', img)
    mean_error = 0
    for i in range(len(points_on_object)):
        imgpoints2, _ = cv2.projectPoints(points_on_object[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(points_on_image[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
        print( "total error: {}".format(mean_error/len(points_on_object)) )
        print(type(ret),type(mtx),type(dist),type(rvecs),type(tvecs))

object_points_test = np.zeros((4*9, 3), np.float32)
object_points_test[:, :2] = np.mgrid[0:4, 0:9].T.reshape(-1, 2)
for frame in image_test:
 img = cv2.imread(frame)
 gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 ret, corners = cv2.findChessboardCorners(gray, (4,9),None)
 if ret == True:
    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    # Find the rotation and translation vectors.
    ret,rvecs, tvecs = cv2.solvePnP(object_points_test, corners2, mtx, dist)
    # project 3D points to image plane
    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

    Rmtx = cv2.Rodrigues(rvecs)

    print(Rmtx[0])
    sy = math.sqrt(Rmtx[0][0][0] * Rmtx[0][0][0] + Rmtx[0][1][0] * Rmtx[0][1][0])
    xAng = math.degrees(math.atan2(Rmtx[0][2][1], Rmtx[0][2][2]))
    yAng = math.degrees(math.atan2(-Rmtx[0][2][0], sy))
    zAng = math.degrees(math.atan2(Rmtx[0][1][0], Rmtx[0][0][0]))
    print(f"xAng = {xAng}, yAng = {yAng}, zAng = {zAng}")
    img = draw(img,corners2,imgpts,xAng,yAng,zAng)
    showMyImage(img,30)
cv2.destroyAllWindows()




"""
for fname in images:
 img = cv2.imread(fname)
 gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 ret, corners = cv2.findChessboardCorners(gray, (6,9),None)
 if ret == True:
    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    # Find the rotation and translation vectors.
    ret,rvecs, tvecs = cv2.solvePnP(object_points, corners2, mtx, dist)
    # project 3D points to image plane
    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

    Rmtx = cv2.Rodrigues(rvecs)

    print(Rmtx[0])
    sy = math.sqrt(Rmtx[0][0][0] * Rmtx[0][0][0] + Rmtx[0][1][0] * Rmtx[0][1][0])
    xAng = math.degrees(math.atan2(Rmtx[0][2][1], Rmtx[0][2][2]))
    yAng = math.degrees(math.atan2(-Rmtx[0][2][0], sy))
    zAng = math.degrees(math.atan2(Rmtx[0][1][0], Rmtx[0][0][0]))
    print(f"xAng = {xAng}, yAng = {yAng}, zAng = {zAng}")
    img = draw(img,corners2,imgpts,xAng,yAng,zAng)
    showMyImage(img,30)
cv2.destroyAllWindows()
"""