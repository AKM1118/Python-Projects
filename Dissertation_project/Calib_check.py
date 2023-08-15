# Takes in an array of corner points of a chessboard, calibration parameters and then compares the effectiveness of calibration parameters
import numpy as np
import cv2
from scipy.spatial import distance
img = cv2.imread('SDC12887.JPG')
r, c = 6, 9
sub_corner_points = np.array([[1344.6705, 1444.8865], [1339.8512, 1372.2052], [1335.1322, 1298.0023], [1330.5327, 1223.1202],

 [1325.7504, 1146.4102], [1321.102,  1067.7146], [1424.5085, 1444.196 ], [1420.5349, 1371.0074], [1416.6116, 1296.8998],

 [1412.6211, 1222.1172], [1408.7604, 1144.8351], [1404.7615, 1066.2888], [1505.056,  1443.1139], [1502.0779, 1370.3401],

 [1498.752,  1295.7163], [1495.5361, 1220.8728], [1492.5769, 1143.4415], [1489.4008, 1064.6051], [1585.8569, 1441.5475],

 [1583.5243, 1368.5197], [1581.2771 ,1294.1792], [1578.7272, 1219.6907], [1576.5256, 1141.8511], [1574.276 , 1062.7164],

 [1666.774,  1440.2692], [1665.2819, 1367.2229], [1663.6385, 1292.8899], [1662.2472, 1218.2493], [1660.6316, 1140.4673],

 [1659.0352 ,1061.2747], [1748.0406, 1438.8097], [1747.1501, 1366.3129], [1746.4902, 1292.1359], [1745.5526, 1216.8611],

 [1744.6969, 1139.1819], [1744.016,  1059.7535], [1828.7325, 1437.3163], [1828.8627 ,1364.71  ], [1828.7762 ,1290.7345],

 [1828.8434, 1215.5898], [1828.8182 ,1138.1333], [1828.6006 ,1057.8097], [1909.1814, 1435.8466], [1910.1339 ,1363.2795],

 [1911.0815 ,1289.3383], [1911.6028,1214.1268], [1912.3912 ,1135.9602], [1912.9475 ,1056.3735], [1989.2694 ,1433.2247],

 [1991.2373 ,1361.5853], [1992.8053 ,1286.9319], [1994.4985, 1211.9098], [1995.678 , 1133.8572], [1997.2303 ,1054.6904]])

ret = 0.7218316116723064

mtx = np.array([[3.52538591e+03, 0.00000000e+00, 1.64924486e+03],
 [0.00000000e+00 ,3.55117301e+03, 1.16745770e+03],
 [0.00000000e+00 ,0.00000000e+00, 1.00000000e+00]])

dist = np.array([-2.77084427e-01,  8.14581003e-01, -1.75902601e-03,  1.31484180e-03, -2.98025019e+00])

rvecs = np.array( [0.01188501,-0.631624  ,3.05759763])

tvecs = np.array([[ 4.21520418,3.28114488,43.48286335]])
print(type(sub_corner_points),type(mtx),type(dist),type(rvecs),type(tvecs))
x_list = np.zeros((9,4))
y_list = np.zeros((6,7))
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
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
undist = cv2.undistort(img, mtx, dist, None, newcameramtx)
imgpoints2, _ = cv2.projectPoints(object_points, rvecs, tvecs, mtx, dist)
print(imgpoints2)

for i in range(c):
 x_st, y_st = imgpoints2[0+r*(i-1)]
 x_end, y_end = imgpoints2[5+r*(i-1)]
 for j in range(r-1):
  xi , yi = imgpoints2[j+r*(i-1)]
  xi_calc = (yi-y_st)*(x_end-x_st)/(y_end-y_st)+x_st
  x_diff = xi - xi_calc
  x_list[i-1][j-1] = x_diff
  print(f"row = {i}, column = {j}, xi = {xi}, x_calc = {xi_calc}")
# yi = (xi-x_st)*(y_end-y_st)/(x_end-x_st)+y_st
print(x_list)

for i in range(r):
 x_st, y_st = imgpoints2[i-1]
 x_end, y_end = imgpoints2[48+i-1]
 for j in range(c-1):
  xi , yi = imgpoints2[6+r*(j-1)+(i-1)]
  yi_calc = (xi-x_st)*(y_end-y_st)/(x_end-x_st)+y_st
  y_diff = yi - yi_calc
  y_list[i-1][j-1] = y_diff
  print(f"row = {i}, column = {j}, yi = {yi}, y_calc = {yi_calc}")
print(y_list)