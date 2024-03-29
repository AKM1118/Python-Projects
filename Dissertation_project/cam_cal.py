# module for camera calibration before the main algorithm
import numpy as np
import cv2
import glob
import math
import time
import xlwt
from functools import wraps
#import Main

#print(Main.a)


def WriteToExcel(sheetName, angle_list, set_number):
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet(f"results")
    sheet1.write(0, 0, "x Angle")
    sheet1.write(0, 1, "y Angle")
    sheet1.write(0, 2, "z Angle")
    for i in range(len(angle_list)):
        x, y, z = angle_list[i]

        sheet1.write(i+1, 0, x)
        sheet1.write(i+1, 1, y)
        sheet1.write(i+1, 2, z)
    workbook.save(f"experiment results 1m calib center {set_number} 15.xls")

def timeToComplete(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print((f"{func} is in process"))
        time_start = time.time()
        val = func(*args, **kwargs)
        time_end = time.time() - time_start
        print((f"{func.__name__} is done in {time_end} s"))
        return val
    return wrapper

def divideImage(images):
    cur_board = 0
    cur_image = 1
    # coordinates table for excess board removal
    coord_dict_p1 = {0 : (1188-50,875+10), 1 : (1531-10, 878+0), 2 : (1866-20, 883+10),
                    3 : (1193-30, 1114+10), 4 : (1530-10, 1117+10), 5 : (1866-20, 1119+10),
                    6 : (1193-30, 1354+30), 7 : (1529-10, 1352+30), 8 : (1865-20, 1354+30)}
    coord_dict_p2 = {0: (1463-50, 1078+10), 1: (1804-10, 1080+0), 2: (2135-20, 1082+10),
                    3: (1467-30, 1317+10), 4: (1801-10, 1318+10), 5: (2134-20, 1318+10),
                    6: (1466-30, 1556+30), 7: (1802-10, 1555+30), 8: (2134-20, 1554+30)}
    for frame in images:
        orig = cv2.imread(frame)
        for cur_board in range(9):
            result = orig.copy()
            for i in coord_dict_p1.keys():
                if i == cur_board:
                    continue
                p1 = coord_dict_p1.get(i)
                p2 = coord_dict_p2.get(i)
                result = cv2.rectangle(result,p1,p2,(125,125,125),thickness=-1)
                #showMyImage(result, 30)

            cv2.imwrite(f"Prepared_Images_5/Image_{cur_board}_{cur_image}.jpg", result)
        print(f"Image {cur_image} is done")
        cur_board = 0
        cur_image += 1

@timeToComplete
def draw(image, corners, imgpts, xAng, yAng, zAng):
 img = cv2.imread(image)
 corner = tuple(corners[0].ravel())
 imgx = tuple(imgpts[0].ravel())
 imgy = tuple(imgpts[1].ravel())
 imgz = tuple(imgpts[2].ravel())
 #print(corner)
 #print(tuple(imgpts[0].ravel()))
 img = cv2.line(img, (int(corner[0]),int(corner[1])), (int(imgx[0]),int(imgx[1])), (0,255,0), 5)
 img = cv2.line(img, (int(corner[0]),int(corner[1])), (int(imgy[0]),int(imgy[1])), (255,0,0), 5)
 img = cv2.line(img, (int(corner[0]),int(corner[1])), (int(imgz[0]),int(imgz[1])), (0,0,255), 5)
 cv2.putText(img, "xAng {:.4f}".format(xAng), ((int(imgx[0]),int(imgx[1]-10))),
             cv2.FONT_HERSHEY_SIMPLEX,3 , (0, 255, 0), 5)
 cv2.putText(img, "yAng {:.4f}".format(yAng), ((int(imgy[0]),int(imgy[1]-10))),
             cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
 cv2.putText(img, "zAng {:.4f}".format(zAng), ((int(imgz[0]),int(imgz[1]+150))),
             cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
 return img
@timeToComplete
def resizeImage(img, scale):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dimensions = (width, height)
    resized_image = cv2.resize(img, dimensions, interpolation=cv2.INTER_AREA)
    return resized_image

def showMyImage(img, scale):
    img_show = img.copy()
    cv2.imshow("Image", resizeImage(img_show,scale))
    cv2.waitKey(0)

@timeToComplete
def getRecalibError(obj_points,img_points,rvecs,tvecs,mtx,dist):
    mean_error = 0
    for i in range(len(obj_points)):
        imgpoints2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(img_points[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error
        print("total error: {}".format(mean_error / len(obj_points)))

@timeToComplete
def getInnerParam(calibration_images=list[str],board_x=int,board_y=int,save_path=str):
    j = 0
    for image in calibration_images:
        print(image)
        j += 1
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (board_y, board_x), None)
        print(f"board {j} is {ret}")
        if ret:
            points_on_object.append(object_points)
            corners_sub_pixel = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            points_on_image.append(corners_sub_pixel)
            cv2.drawChessboardCorners(img, (board_y, board_x), corners, ret)

    # extracting calibration parameters from calibration images
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(points_on_object, points_on_image, gray.shape[::-1], None, None)
    np.savez(save_path, mtx=mtx, dist=dist)
    print(f"mtx = {mtx} # "
          f"dist = {dist} # ")
    getRecalibError(points_on_object,points_on_image,rvecs,tvecs,mtx,dist)

@timeToComplete
def getAngles(rvecs):
    Rmtx = cv2.Rodrigues(rvecs)
    # print(Rmtx[0])
    sy = math.sqrt(Rmtx[0][0][0] * Rmtx[0][0][0] + Rmtx[0][1][0] * Rmtx[0][1][0])
    xAng = math.degrees(math.atan2(Rmtx[0][2][1], Rmtx[0][2][2]))
    yAng = math.degrees(math.atan2(-Rmtx[0][2][0], sy))
    zAng = math.degrees(math.atan2(Rmtx[0][1][0], Rmtx[0][0][0]))
    print(f"xAng = {xAng} type {type(xAng)}, yAng = {yAng} type {type(yAng)}, zAng = {zAng} type {type(zAng)}")
    return xAng, yAng, zAng

@timeToComplete
def getCorners(image,board_x,board_y):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (board_y, board_x), None)
    print(ret)
    return ret,corners, gray

@timeToComplete
def main():

    # Uncomment this if you want to generate new sets
    #print(glob.glob(board_img_path))
    #board_images = glob.glob(board_img_path)
    #divideImage(board_images)
    #return

    try:
        cam_params = np.load(calib_param_path)
    except OSError:
        print('No inner parameters found, trying to calculate new ones...')
        calib_images = glob.glob(calib_img_path)
        if calib_images == []:
            raise Exception('No calibration images found, please choose a different folder')
        getInnerParam(calib_images,board_x_cal,board_y_cal,save_path)
        cam_params = np.load(calib_param_path)


    mtx = cam_params['mtx']
    dist = cam_params['dist']
    #mtx = np.array([[3.432e+03, 0, 1.62588e+03], [0, 3.456e+03, 2.20795e+03], [0, 0, 1]], dtype=np.float64)
    #dist = np.array([0,0,0,0,0], dtype=np.float64)
    print(f"mtx = {mtx} # "
          f"dist = {dist} # ")
    i = 1
    k = 1
    #experiment_img = glob.glob(experiment)
    image_test = glob.glob(detect_img_path)
    object_points = np.zeros((board_y_detect * board_x_detect, 3), np.float32)
    object_points[:, :2] = np.mgrid[0:board_y_detect, 0:board_x_detect].T.reshape(-1, 2)
    #i = 1

    experiment_img = glob.glob(experiment)
    xArr = []
    yArr = []
    zArr = []

    for k in range(1,10):
        angle_arr = []
        experiment_img = glob.glob(f'Set_1_{k}/*.jpg')
        i = 1
        for frame in experiment_img:
            ret, corners, gray = getCorners(frame, board_x_detect, board_y_detect)
            img = cv2.imread(frame)
            print(ret)
            if ret == True:
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            # Find the rotation and translation vectors.
                ret, rvecs, tvecs = cv2.solvePnP(object_points, corners2, mtx, dist)
                #ret, rvecs, tvecs = cv2.solvePnP(object_points, corners2, mtx, dist, flags=cv2.SOLVEPNP_EPNP)

            # project 3D points to image plane
                imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
                xAng, yAng, zAng = getAngles(rvecs)
            #xArr.append(xAng)
            #yArr.append(yAng)
            #zArr.append(zAng)
                angle_arr.append((xAng, yAng, zAng))
            #h, w = img.shape[:2]
            #object_points = np.zeros((6 * 9, 3), np.float32)
            #object_points[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
            #print("###### optimizing the matrix ######")
            #newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
            #undist = cv2.undistort(img, mtx, dist, None, newcameramtx)
            #imgpoints2, _ = cv2.projectPoints(object_points, rvecs, tvecs, mtx, dist)
            #img = draw(undist, corners2, imgpts, xAng, yAng, zAng)
            #img = draw(frame, corners2, imgpts, xAng, yAng, zAng)
            #showMyImage(img, 30)
            print(f"image {i} is done")
            i += 1
        print(f"set {k} is done")
        WriteToExcel("results",angle_arr,k)


    # for frame in experiment_img:
    #     ret, corners, gray = getCorners(frame, board_x_detect, board_y_detect)
    #     img = cv2.imread(frame)
    #     if ret == True:
    #         corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    #
    #         # Find the rotation and translation vectors.
    #         ret, rvecs, tvecs = cv2.solvePnP(object_points, corners2, mtx, dist)
    #
    #         # project 3D points to image plane
    #         imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
    #         xAng, yAng, zAng = getAngles(rvecs)
    #         angle_arr.append((xAng, yAng, zAng))
    #         img = draw(frame, corners2, imgpts, xAng, yAng, zAng)
    #         showMyImage(img, 30)
    #         print(f"image {i} is done")
    #         i += 1
    # WriteToExcel(workbook,"results",angle_arr)
    #for frame in image_test:
    #    ret, corners, gray = getCorners(frame,board_x_detect,board_y_detect)
    #    img = cv2.imread(frame)
    #    if ret == True:
    #        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
#
 #           # Find the rotation and translation vectors.
 #           ret, rvecs, tvecs = cv2.solvePnP(object_points, corners2, mtx, dist)
#
#            # project 3D points to image plane
#            imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
#            xAng, yAng, zAng = getAngles(rvecs)
#            img = draw(frame, corners2, imgpts, xAng, yAng, zAng)
#            showMyImage(img, 30)
#            # showMyImage(cp, 30)
    cv2.destroyAllWindows()

# Constants

# board size for x and y
board_x_cal = 10
board_y_cal = 7

board_x_detect = 10
board_y_detect = 7
# criteria for sub pixel corner detection
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# creating arrays to store all found corner points
object_points = np.zeros((board_y_cal*board_x_cal, 3), np.float32)
object_points[:, :2] = np.mgrid[0:board_y_cal, 0:board_x_cal].T.reshape(-1, 2)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

# arrays where we store points from processed images
points_on_object = []
points_on_image = []

# file paths for calibration and detection
calib_img_path = 'New_calibphotos_1/*.jpg'
calib_param_path = 'cam_param_center_1m.npz'
detect_img_path = 'Dist_detect_5/*.JPG'
save_path = 'cam_param_center_1m'

# file paths for experiments
#experiment = 'Prepared_Images/Set_4/*.jpg'
experiment = 'Set_0_5/*.jpg'
#experiment = 'New_calibphotos_3/*.jpg'
# file paths for experiments
#board_img_path = '9_boards_90_photos/*.jpg'
board_img_path = '9_boards_100_photos_15/*.jpg'
# excel base for writing


# array to store angle values
angle_arr = []

if __name__ == "__main__":
    main()


"""
for fname in images:
 img = cv2.imread(fname)
 gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 ret, corners = cv2.findChessboardCorners(gray, (4,7),None)
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
 else:
    showMyImage(img, 10)
cv2.destroyAllWindows()
"""