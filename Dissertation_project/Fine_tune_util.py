# A GUI to test out how different intrinsic parameters affect calculated angles
import cam_cal
import numpy as np
import cv2
import glob
import math
import time
import xlwt
from functools import wraps

# TODO: create a simple GUI with trackbars to visualise fine-tuning
def WriteToExcel(sheetName, angle_list, set_number):
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet(f"results")
    sheet1.write(0, 0, "x Angle")
    sheet1.write(0, 1, "y Angle")
    sheet1.write(0, 2, "z Angle")
    sheet1.write(0, 3, f"param {set_number}")
    for i in range(len(angle_list)):
        x, y, z, p = angle_list[i]

        sheet1.write(i+1, 0, x)
        sheet1.write(i+1, 1, y)
        sheet1.write(i +1, 2, z)
        sheet1.write(i + 1, 3, p)
    workbook.save(f"{sheetName} {set_number}.xls")

def getParamArray(param,steps):
    param_array = []
    step_val = param/steps
    param_array.append(param)
    for i in range(0,int(steps/10)):
        param_array.append(param + i * step_val)
        param_array.append(param - i * step_val)
    param_array.sort()
    return param_array


calib_param_path = 'cam_param.npz'
cam_params = np.load(calib_param_path)
mtx = cam_params['mtx']
dist = cam_params['dist']
#mtx = np.array([[1 ,0,1],[0,1 ,1],[0,0,1]], dtype=np.float64)
print(f"mtx = {mtx} # "
          f"dist = {dist} # ")
#mtx = np.array([[3.332671e+03 ,0,1.60978633e+03],[0,3.45279984e+03 ,1.21315992e+03],[0,0,1]], dtype=np.float64)
#mtx = np.array([[1 ,0,1],[0,1 ,1],[0,0,1]], dtype=np.float64)
#dist = np.array([0,0,0,0,0], dtype=np.float64)
def getResults(param_list,experiment_number):
    for param in param_list:
        i = param_list.index(param)
        cam_params = np.load(calib_param_path)
        #mtx = np.array([[3.332671e+03, 0, 1.60978633e+03], [0, 3.45279984e+03, 1.21315992e+03], [0, 0, 1]],
        #               dtype=np.float64)
        mtx = np.array([[3.432e+03, 0, 1.62588e+03], [0, 3.456e+03, 2.20795e+03], [0, 0, 1]], dtype=np.float64)
        #mtx = np.array([[3.332671e+03, 0, 1], [0, 1, 1], [0, 0, 1]], dtype=np.float64)
        #mtx = np.array([[1, 0, 1], [0, 1, 1], [0, 0, 1]], dtype=np.float64)
        #mtx = cam_params['mtx']
        # dist = cam_params['dist']
        angle_arr = []
        for j in range(len(param)):
            if i == 0:
                mtx[0][0] = param[j]
            if i == 1:
                mtx[1][1] = param[j]
            if i == 2:
                mtx[0][2] = param[j]
            if i == 3:
                mtx[1][2] = param[j]

            ret, rvecs, tvecs = cv2.solvePnP(object_points, corners2, mtx, dist)
            imgpts, _ = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            xAng, yAng, zAng = cam_cal.getAngles(rvecs)
            angle_arr.append((xAng, yAng, zAng, param[j]))
            #frame = cam_cal.draw(test_image, corners2, imgpts, xAng, yAng, zAng)
            print(f"param {i} is {param[j]}")
            #cam_cal.showMyImage(frame, 30)
        if i == 0:
            WriteToExcel("param_experiment fx", angle_arr, experiment_number)
        if i == 1:
            WriteToExcel("param_experiment fy", angle_arr, experiment_number)
        if i == 2:
            WriteToExcel("param_experiment cx", angle_arr, experiment_number)
        if i == 3:
            WriteToExcel("param_experiment cy", angle_arr, experiment_number)

fx_array = getParamArray(mtx[0][0],1000)
fy_array = getParamArray(mtx[1][1],1000)
cx_array = getParamArray(mtx[0][2],1000)
cy_array = getParamArray(mtx[1][2],1000)

param_list = [fx_array,fy_array,cx_array,cy_array]

board_x_detect = 10
board_y_detect = 7

object_points = np.zeros((board_y_detect * board_x_detect, 3), np.float32)
object_points[:, :2] = np.mgrid[0:board_y_detect, 0:board_x_detect].T.reshape(-1, 2)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

points_on_object = []
points_on_image = []

test_image = 'Set_1_0/Image_4_3.jpg'

ret, corners, gray = cam_cal.getCorners(test_image, board_x_detect, board_y_detect)
img = cv2.imread(test_image)
corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

getResults(param_list, 20)




