# Takes in an array of corner points of a chessboard, calibration parameters and then compares the effectiveness of calibration parameters
import glob

import numpy as np
import cv2
import xlwt
from xlwt import Workbook


def WriteToExcel(workbook, sheetName, x_list, y_list, x_list1, y_list1):
 sheet1 = workbook.add_sheet(sheetName)
 for i in range(len(x_list)):
  for j in range(len(x_list[i])):
   sheet1.write(i,j, x_list[i,j])
   sheet1.write(i+20,j,x_list1[i,j])
 for i in range(len(y_list)):
  for j in range(len(y_list[i])):
   sheet1.write(i, j+20, y_list[i, j])
   sheet1.write(i + 20, j+20, y_list1[i, j])
 workbook.save("deviation results.xls")
def GetUndistorted(img,mtx,dist,Debug=False):
 w, h = img.shape[:2]
 newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
 undist = cv2.undistort(img, mtx, dist, None, newcameramtx)
 if Debug:
  scale_percent = 55  # percent of original size
  width = int(undist.shape[1] * scale_percent / 100)
  height = int(undist.shape[0] * scale_percent / 100)
  dim = (width, height)
  resized = cv2.resize(undist, dim, interpolation=cv2.INTER_AREA)
  cv2.imshow('img', resized)
  cv2.waitKey(0)
 return undist
def GetSubCornerPoints(img,rows,columns,Debug=False):
 criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 ret, corners = cv2.findChessboardCorners(gray, (rows, columns), None)
 corners_sub_pixel = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
 if Debug:
  print("#######sub_pix_corners#########")
  print(corners_sub_pixel)
  print("##########################")
 return corners_sub_pixel
def GetDeviation(sub_corner_points,rows,columns,Debug=False): # Calculates deviation on x & y axies and return two arrays of deviations for each point
 r = rows
 c = columns
 x_list = np.zeros((c, r-2))
 y_list = np.zeros((r, c-2))
 for i in range(c):
  coord = sub_corner_points[0 + r * (i - 1)]
  x_st, y_st = coord [0,0],coord[0,1]
  coord = sub_corner_points[5 + r * (i - 1)]
  x_end, y_end = coord [0,0],coord[0,1]
  for j in range(r - 1):
   coord = sub_corner_points[j + r * (i - 1)]
   xi, yi = coord [0,0],coord[0,1]
   xi_calc = (yi - y_st) * (x_end - x_st) / (y_end - y_st) + x_st
   x_diff = xi - xi_calc
   x_list[i - 1][j - 1] = x_diff

 for i in range(r):
  coord = sub_corner_points[i - 1]
  x_st, y_st = coord [0,0],coord[0,1]
  coord = sub_corner_points[48 + i - 1]
  x_end, y_end = coord [0,0],coord[0,1]
  for j in range(c - 1):
   coord = sub_corner_points[6 + r * (j - 1) + (i - 1)]
   xi, yi = coord [0,0],coord[0,1]
   yi_calc = (xi - x_st) * (y_end - y_st) / (x_end - x_st) + y_st
   y_diff = yi - yi_calc
   y_list[i - 1][j - 1] = y_diff
 if Debug:
  print("##########x_list############")
  print(x_list)
  print("##########y_list############")
  print(y_list)
  print("############################")
 return x_list, y_list
def CalculateImage(img,mtx,dist,rows,columns):
 sub_corner_points = GetSubCornerPoints(img,rows,columns)
 x_list, y_list = GetDeviation(sub_corner_points, r, c)
 undist_img = GetUndistorted(img,mtx,dist,True)
 sub_corner_points_un = GetSubCornerPoints(undist_img,rows,columns)
 x_list_un, y_list_un = GetDeviation(sub_corner_points_un,rows,columns)
 return x_list, y_list, x_list_un, y_list_un
images = glob.glob('*.jpg')

# img = cv2.imread('SDC12887.JPG')
r, c = 6, 9
# sub_corner_points = np.array([[1344.6705, 1444.8865], [1339.8512, 1372.2052], [1335.1322, 1298.0023], [1330.5327, 1223.1202],
#
# [1325.7504, 1146.4102], [1321.102,  1067.7146], [1424.5085, 1444.196 ], [1420.5349, 1371.0074], [1416.6116, 1296.8998],
#
# [1412.6211, 1222.1172], [1408.7604, 1144.8351], [1404.7615, 1066.2888], [1505.056,  1443.1139], [1502.0779, 1370.3401],
#
# [1498.752,  1295.7163], [1495.5361, 1220.8728], [1492.5769, 1143.4415], [1489.4008, 1064.6051], [1585.8569, 1441.5475],
#
# [1583.5243, 1368.5197], [1581.2771 ,1294.1792], [1578.7272, 1219.6907], [1576.5256, 1141.8511], [1574.276 , 1062.7164],
#
# [1666.774,  1440.2692], [1665.2819, 1367.2229], [1663.6385, 1292.8899], [1662.2472, 1218.2493], [1660.6316, 1140.4673],
#
# [1659.0352 ,1061.2747], [1748.0406, 1438.8097], [1747.1501, 1366.3129], [1746.4902, 1292.1359], [1745.5526, 1216.8611],
#
# [1744.6969, 1139.1819], [1744.016,  1059.7535], [1828.7325, 1437.3163], [1828.8627 ,1364.71  ], [1828.7762 ,1290.7345],
#
# [1828.8434, 1215.5898], [1828.8182 ,1138.1333], [1828.6006 ,1057.8097], [1909.1814, 1435.8466], [1910.1339 ,1363.2795],
#
# [1911.0815 ,1289.3383], [1911.6028,1214.1268], [1912.3912 ,1135.9602], [1912.9475 ,1056.3735], [1989.2694 ,1433.2247],
#
# [1991.2373 ,1361.5853], [1992.8053 ,1286.9319], [1994.4985, 1211.9098], [1995.678 , 1133.8572], [1997.2303 ,1054.6904]])


ret = 0.7218316116723064

mtx = np.array([[3.52538591e+03, 0.00000000e+00, 1.64924486e+03],
 [0.00000000e+00 ,3.55117301e+03, 1.16745770e+03],
 [0.00000000e+00 ,0.00000000e+00, 1.00000000e+00]])

dist = np.array([-2.77084427e-01,  8.14581003e-01, -1.75902601e-03,  1.31484180e-03, -2.98025019e+00])


rvecs = np.array( [0.01188501,-0.631624  ,3.05759763])

tvecs = np.array([[ 4.21520418,3.28114488,43.48286335]])

x_list = np.zeros((9,4))
y_list = np.zeros((6,7))
x_list1 = np.zeros((9,4))
y_list1 = np.zeros((6,7))

workbook = xlwt.Workbook()
style = xlwt.easyxf('font: bold 1')
k = 1
print(f"total images = {len(images)}")
for fname in images:
 img = cv2.imread(fname)
 x_list, y_list, x_list1, y_list1 = CalculateImage(img,mtx,dist,r,c)
 print(f"Writing image {k}")
 WriteToExcel(workbook,f"image {k}",x_list,y_list,x_list1,y_list1)
 print(f"Image {k} is done")
 k += 1

"""
print("###### calculating x points for sub ######")
for i in range(c):
 x_st, y_st = sub_corner_points[0+r*(i-1)]
 x_end, y_end = sub_corner_points[5+r*(i-1)]
 for j in range(r-1):
  xi , yi = sub_corner_points[j+r*(i-1)]
  xi_calc = (yi-y_st)*(x_end-x_st)/(y_end-y_st)+x_st
  x_diff = xi - xi_calc
  x_list[i-1][j-1] = x_diff
  print(f"row = {i}, column = {j}, xi = {xi}, x_calc = {xi_calc}")
# yi = (xi-x_st)*(y_end-y_st)/(x_end-x_st)+y_st
print(x_list)
print("###### calculating y points for sub ######")
for i in range(r):
 x_st, y_st = sub_corner_points[i-1]
 x_end, y_end = sub_corner_points[48+i-1]
 for j in range(c-1):
  xi , yi = sub_corner_points[6+r*(j-1)+(i-1)]
  yi_calc = (xi-x_st)*(y_end-y_st)/(x_end-x_st)+y_st
  y_diff = yi - yi_calc
  y_list[i-1][j-1] = y_diff
  print(f"row = {i}, column = {j}, yi = {yi}, y_calc = {yi_calc}")
print(y_list)

h, w = img.shape[:2]
object_points = np.zeros((6*9, 3), np.float32)
object_points[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
print("###### optimizing the matrix ######")
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
undist = cv2.undistort(img, mtx, dist, None, newcameramtx)
imgpoints2, _ = cv2.projectPoints(object_points, rvecs, tvecs, mtx, dist)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, corners = cv2.findChessboardCorners(gray, (6, 9), None)

if ret:
 cv2.drawChessboardCorners(img, (6, 9), corners, ret)
 for i in range(len(corners)):
  coord = corners[i]
  x_old = coord[0,0]
  y_old = coord[0,1]
  cv2.circle(img, (int(x_old), int(y_old)), 1, (175+i,39+i, 45+i), -1)
  cv2.putText(img, "{}".format(i),(int(x_old - 50), int(y_old - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (39+i, 172+i, 45+i), 2)


gray = cv2.cvtColor(undist,cv2.COLOR_BGR2GRAY)
ret, corners = cv2.findChessboardCorners(gray, (6, 9), None)
corners_sub_pixel = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
print("###### drawing points on a new image ######")
if ret:
 cv2.drawChessboardCorners(undist, (6, 9), corners, ret)
 for i in range(len(imgpoints2)):
  coord = imgpoints2[i]
  x_new = coord[0,0]
  y_new = coord[0,1]
  # cv2.circle(undist, (int(x), int(y)), 8, (175+i,39+i, 45+i), -1)
  cv2.circle(undist, (int(x_new), int(y_new)), 1, (128 + i, 128 + i, 128 + i), -1)
  cv2.circle(img, (int(x_new), int(y_new)), 1, (128 + i, 128 + i, 128 + i), -1)
  cv2.putText(undist, "{}".format(i),(int(x_new - 50), int(y_new - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (45+i, 39+i, 175+i), 2)

  coord = corners_sub_pixel[i]
  x_new = coord[0, 0]
  y_new = coord[0, 1]
  cv2.circle(undist, (int(x_new), int(y_new)), 1, (168 + i, 55 + i, 12 + i), -1)
print("############### writing cal2 image #############")
cv2.imwrite('calbka_2.png', undist)
cv2.imwrite('calbka_1.png', img)
print("###### calculating x points for undist ######")
for i in range(c):
 coord = corners_sub_pixel[0+r*(i-1)]
 x_st, y_st = coord[0,0], coord[0,1]
 coord = corners_sub_pixel[5+r*(i-1)]
 x_end, y_end = coord[0,0], coord[0,1]
 for j in range(r-1):
  coord = corners_sub_pixel[j+r*(i-1)]
  xi , yi = coord[0,0], coord[0,1]
  xi_calc = (yi-y_st)*(x_end-x_st)/(y_end-y_st)+x_st
  x_diff = xi - xi_calc
  x_list1[i-1][j-1] = x_diff
  print(f"row = {i}, column = {j}, xi = {xi}, x_calc = {xi_calc}")
print(x_list1)
print("###### calculating y points for undist ######")
for i in range(r):
 coord = corners_sub_pixel[i-1]
 x_st, y_st = coord[0,0], coord[0,1]
 coord = corners_sub_pixel[48+i-1]
 x_end, y_end = coord[0,0], coord[0,1]
 for j in range(c-1):
  coord = corners_sub_pixel[6+r*(j-1)+(i-1)]
  xi , yi = coord[0,0], coord[0,1]
  yi_calc = (xi-x_st)*(y_end-y_st)/(x_end-x_st)+y_st
  y_diff = yi - yi_calc
  y_list1[i-1][j-1] = y_diff
  print(f"row = {i}, column = {j}, yi = {yi}, y_calc = {yi_calc}, proj_point = {6+r*(j-1)+(i-1)}")
print(y_list1)

#for i in range(c):
# x_y_st = imgpoints2[i-1]/2
# x_y_end = imgpoints2[5+r*(i-1)]
# print(type(x_y_st),x_y_st,type(x_y_end),x_y_end)
# for j in range(r-1):
#  xi_yi = imgpoints2[j+r*(i-1)]
#  xi_calc1 = (xi_yi[1]-x_y_st[1])*(x_y_end[0]-x_y_st[0])/(x_y_end[1]-x_y_st[1])+x_y_st[0]
#  x_diff1 = xi_yi[0] - xi_calc1
#  x_list1[i-1][j-1] = x_diff1
#  print(f"row = {i}, column = {j}, xi = {xi_yi}, x_calc = {xi_calc1}")
# yi = (xi-x_st)*(y_end-y_st)/(x_end-x_st)+y_st
#print(x_list1)

#for i in range(r):
# x_st2, y_st2 = imgpoints2[i-1], imgpoints2[i-1]
# x_end2, y_end2 = imgpoints2[48+i-1]
# for j in range(c-1):
#  xi2 , yi2 = imgpoints2[6+r*(j-1)+(i-1)]
#  yi_calc2 = (xi2-x_st2)*(y_end2-y_st2)/(x_end2-x_st2)+y_st2
#  y_diff2 = yi2 - yi_calc2
#  y_list1[i-1][j-1] = y_diff2
#  print(f"row = {i}, column = {j}, yi = {yi2}, y_calc = {yi_calc2}")
#print(y_list1)
"""