# Takes in an array of corner points of a chessboard, calibration parameters and then compares the effectiveness of calibration parameters
import numpy as np
import cv2
from scipy.spatial import distance
img = cv2.imread('SDC12887.JPG')
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
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

#projected_corners = np.array([[1989.691,  1434.2527], [1909.1166, 1435.8796], [1828.3912, 1437.4315], [1747.5769, 1438.904 ],
# [1666.7395, 1440.2941], [1585.9469, 1441.5995], [1505.2675, 1442.8201], [1424.7672, 1443.9564], [1344.5089, 1445.0107],
# [1991.3878, 1361.513 ], [1910.0182, 1363.1106], [1828.4905, 1364.6506], [1746.8694, 1366.1293], [1665.2235, 1367.5438],
# [1583.6238, 1368.8925], [1502.1415, 1370.1743], [1420.8456, 1371.3899], [1339.8011, 1372.5405], [1993.0471, 1287.2799],
# [1910.8833, 1288.8429], [1828.5552, 1290.3672], [1746.1295, 1291.8499], [1663.6776, 1293.2888], [1581.2734,1294.6823],
# [1498.9907, 1296.0293], [1416.9014,1297.3296], [1335.0726, 1298.5839], [1994.6625, 1211.5581], [1911.7072, 1213.0813],
# [1828.5818, 1214.5863], [1745.3555, 1216.0714], [1662.1019, 1217.5347], [1578.8975, 1218.9746], [1495.8187, 1220.3903],
# [1412.9397, 1221.7806], [1330.33,   1223.1451], [1996.2281, 1134.3579], [1912.4852, 1135.837 ], [1828.5675, 1137.32  ],
# [1744.546,  1138.8058], [1660.4967, 1140.2936], [1576.4982, 1141.7817], [1492.629,  1143.2692], [1408.9656, 1144.754 ],
# [1325.5792, 1146.2349], [1997.7394, 1055.6948], [1913.2137, 1057.1268], [1828.5099, 1058.5856], [1743.7002, 1060.0713],
# [1658.8624, 1061.5837], [1574.0771, 1063.1217], [1489.4249, 1064.6836], [1404.9836, 1066.267 ], [1320.8264, 1067.8691]])

projected_corners = np.array([[1320.8264, 1067.8691],[1404.9836, 1066.267 ], [1489.4249, 1064.6836], [1574.0771, 1063.1217],[1658.8624, 1061.5837],
 [1743.7002, 1060.0713], [1828.5099, 1058.5856], [1913.2137, 1057.1268], [1997.7394, 1055.6948], [1325.5792, 1146.2349],
 [1408.9656, 1144.754 ], [1492.629,  1143.2692], [1576.4982, 1141.7817], [1660.4967, 1140.2936], [1744.546,  1138.8058],
 [1828.5675, 1137.32  ], [1912.4852, 1135.837 ], [1996.2281, 1134.3579], [1330.33,   1223.1451], [1412.9397, 1221.7806],
 [1495.8187, 1220.3903], [1578.8975, 1218.9746], [1662.1019, 1217.5347], [1745.3555, 1216.0714], [1828.5818, 1214.5863],
 [1911.7072, 1213.0813], [1994.6625, 1211.5581], [1335.0726, 1298.5839], [1416.9014,1297.3296],  [1498.9907, 1296.0293],
 [1581.2734,1294.6823],  [1663.6776, 1293.2888], [1746.1295, 1291.8499], [1828.5552, 1290.3672], [1910.8833, 1288.8429],
 [1993.0471, 1287.2799], [1339.8011, 1372.5405], [1420.8456, 1371.3899], [1502.1415, 1370.1743], [1583.6238, 1368.8925],
 [1665.2235, 1367.5438], [1746.8694, 1366.1293], [1828.4905, 1364.6506], [1910.0182, 1363.1106], [1991.3878, 1361.513 ],
 [1344.5089, 1445.0107], [1424.7672, 1443.9564], [1505.2675, 1442.8201], [1585.9469, 1441.5995], [1666.7395, 1440.2941],
 [1747.5769, 1438.904 ], [1828.3912, 1437.4315], [1909.1166, 1435.8796], [1989.691,  1434.2527]
          ])
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