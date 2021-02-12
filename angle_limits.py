import numpy as np 
import matplotlib.pyplot as plt
from scipy import optimize
from sympy import *


## Data
# -1 indicates that there was no limit
# [shoulder_angle, elbow_angle_limit, wrist_angle_limit]
vals = np.array([
    [150,180,145],
    [140,180,-1],
    [180,132,90],
    [160, 151, 90],
    [150, 168, 90],
    [145, 176, 90],
    [180, 123, 0],
    [180, 142, 180],
    [160, 163, 180],
    [170, 145, 180],
    [170, 125, 0] ,
    [160, 140, 0],
    [150, 162, 0],
    [0, 60, 90],
    [20, 58, 90],
    [30, 42, 90],
    [40, 24, 90]
])
s_angles = vals[:, :1]
e_angles = vals[:, 1:2]
w_angles = vals[:, 2:3] 
shoulder_angles_g140 = np.array([180,160,150,145])
shoulder_angles_l40 = np.array([0,20,30,40])
elbow_angle_limits_g140 = np.array([134, 151, 168, 176])
elbow_angle_limits_l40 = np.array([60,58,42,24])


## Equation fitting
coeffs_linear_g140 = np.polyfit(shoulder_angles_g140, elbow_angle_limits_g140, deg=1)
coeffs_quad_g140 = np.polyfit(shoulder_angles_g140, elbow_angle_limits_g140, deg=2)
coeffs_linear_l40 = np.polyfit(shoulder_angles_l40, elbow_angle_limits_l40, deg=1)
coeffs_quad_l40 = np.polyfit(shoulder_angles_l40, elbow_angle_limits_l40, deg=2)

# print(coeffs)
# print(coeffs2)
# print(coeffsb)
# print(coeffs2b)

def fitted(x, coeffs, opt='linear'):
    if opt == 'quad':
        return coeffs[0]*(x**2) + coeffs[1]*x + coeffs[2]
    return coeffs[0]*x + coeffs[1]
  

xvec_g140 = np.linspace(140, 180, 100)
yvec_linear_g140 = fitted(xvec_g140, coeffs_linear_g140)
yvec_quad_g140 = fitted(xvec_g140, coeffs_quad_g140 ,opt='quad')

xvec_l40 = np.linspace(0, 40, 100)
yvec_linear_l40 = fitted(xvec_l40, coeffs_linear_l40)
yvec_quad_l40 = fitted(xvec_l40, coeffs_quad_l40 ,opt='quad')

## Plotting
fig = plt.figure(num=1, clear=True)
ax = fig.add_subplot(1, 1, 1)
ax.plot(shoulder_angles_g140, elbow_angle_limits_g140, 'c.')
ax.plot(xvec_g140, yvec_linear_g140, 'k-')
ax.plot(xvec_g140, yvec_quad_g140, 'r-')
ax.set_xlabel('Shoulder Angles')
ax.set_ylabel('Elbow Angle Maximums')

fig2 = plt.figure(num=2, clear=True)
ax2 = fig2.add_subplot(1, 1, 1)
ax2.plot(shoulder_angles_l40, elbow_angle_limits_l40, 'c.')
ax2.plot(xvec_l40, yvec_linear_l40, 'k-')
ax2.plot(xvec_l40, yvec_quad_l40, 'r-')
ax2.set_xlabel('Shoulder Angles')
ax2.set_ylabel('Elbow Angle Minimums')

fig3 = plt.figure(num=3, clear=True)
ax3 = fig3.add_subplot(1,1,1, projection='3d' )
ax3.scatter(s_angles, e_angles, w_angles)
ax3.set_xlabel('Shoulder Angles')
ax3.set_ylabel('Elbow Angles')
ax3.set_zlabel('Wrist Angles')

plt.show()

# # Attempts to fit to sine curve and a trig derivation

# def sin_func(x, a, b):
#     return a * np.cos(b * x)

# def derivation(x, *coefs):
#     return asin(coefs[0] * sin(x)) + 90 + x

# popt = optimize.curve_fit(sin_func, shoulder_angles, elbow_angle_limits)[0]
# popt2 = optimize.curve_fit(sin_func, shoulder_angles2, elbow_angle_limits2)[0]
# print(popt)

# ysinvec = sin_func(xvec, popt[0], popt[1])
# #ax.plot(xvec, ysinvec, 'r-')
# ysinvec2 = sin_func(xvec2, popt2[0], popt2[1])
#ax2.plot(xvec2, ysinvec2, 'r-')


# color_code = {90: 'red', 145: 'black', 180: 'blue', 0: 'orange', -1: 'yellow'}

# s_angles_w90 = list()
# e_angles_w90 = list()
# labels = []
# for i in range(len(s_angles)):
#     print(w_angles[i])
#     if w_angles[i] == 90 and e_angles[i] != -1:
#         print("HERE")
#         labels += [w_angles[i]]
#         s_angles_w90.append(s_angles[i])
#         e_angles_w90.append(e_angles[i])
# ax.scatter(s_angles_w90, e_angles_w90)
# i = 0
# for x,y in zip(s_angles_w90,e_angles_w90):

#     label = labels[i]

#     plt.annotate(label, # this is the text
#                  (x,y), # this is the point to label
#                  textcoords="offset points", # how to position the text
#                  xytext=(0,10), # distance from text to points (x,y)
#                  ha='center') # horizontal alignment can be left, right or center
#     i += 1

# #ax.plot(xvec, yvec2, 'r-')
# plt.show()

# l1, l2, b1 = symbols('l1 l2 b1')
# theta = asin((l1/l2 * sin(b1)) + 90 + b1)