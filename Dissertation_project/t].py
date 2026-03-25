import numpy as np

cam_params = np.load('cam_param_new.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
mtx = np.array([[3.432e+03, 0, 1.62588e+03], [0, 3.456e+03, 2.20795e+03], [0, 0, 1]], dtype=np.float64)
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")
cam_params = np.load('cam_param_1_m_old.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")
cam_params = np.load('cam_param_3_m_old.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")
cam_params = np.load('Matlab_1m_all.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")
cam_params = np.load('Matlab_1m_reduced.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")
cam_params = np.load('Matlab_3m_all.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")
cam_params = np.load('Matlab_3m_reduced.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")

#mtx = np.array([[4236.75632166584, 30.3575401283590, 1900.53886536036], [0, 4265.19576994639, 1506.67294814716], [0, 0, 1]], dtype = np.float32)
#dist = np.array([-0.106185807759613,  -1.71043609423637, 0.00792718594007832,  0.00817264339260676, 12.2127043960788], dtype = np.float32)
#np.savez('cam_param_center_3m_matlab', mtx=mtx, dist=dist)
cam_params = np.load('cam_param_center_3m_matlab.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")

cam_params = np.load('cam_param_center_3m.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")

cam_params = np.load('cam_param_center_1m_matlab.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")

cam_params = np.load('cam_param_center_1m.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")

#mtx = np.array([[3853.62174175880, 21.1547396845242, 1562.96914209242],[0, 3882.62951950438, 1045.09234589959],[0,0,1]], dtype=np.float64)
#dist = np.array([-0.126241380149709,	0.272187646566270, -0.0127037546533034,	-0.00653544678547856, -0.764005659609455], dtype=np.float64)
#np.savez('cam_param_1_m_new', mtx=mtx, dist=dist)

mtx = np.array([[3607.99983142619, 0, 1532.18178866451],[0, 3640.49110422093, 1183.94156012857],[0,0,1]], dtype=np.float64)
dist = np.array([-0.1811499923126079,0.229932551088108, -0.00144045391410413, -0.00814095454145998, 0], dtype=np.float64)
np.savez('cam_param_opt_matlab', mtx=mtx, dist=dist)

cam_params = np.load('cam_param_opt_matlab.npz')
mtx = cam_params['mtx']
dist = cam_params['dist']
print(f"mtx = {mtx} # ")
print(f"dist = {dist} # ")