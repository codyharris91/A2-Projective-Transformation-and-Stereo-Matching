###################################
# CS B657 Spring 2021, Assignment #1
# 
# Part 1: Homography
#
# Cody Harris
# Neelan Schueman
# Emma Cai
#
# OpenCV Ideas for annotation taken from:
# https://automaticaddison.com/how-to-annotate-images-using-opencv/
# Some small snippets of code are directly copied, and some ideas
# are applied from the sample code.

import sys
import os
import cv2
import numpy as np
from PIL import Image

def draw_circle(event, x, y, flags, param):
    height = param[0].shape[0]
    width = param[0].shape[1]
 
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(param[0], (x, y), 5, (255, 0, 0), -1)
 
        # Append values to the list
        param[1].append(x)
        param[2].append(y)

def make_xy(x,y):
    x = np.array(x)
    y = np.array(y)
    left_ind = x.argsort()[:2]
    right_ind = x.argsort()[2:]
    left_points = [(x[left_ind[0]], y[left_ind[0]]), (x[left_ind[1]], y[left_ind[1]])]
    right_points = [(x[right_ind[0]], y[right_ind[0]]), (x[right_ind[1]], y[right_ind[1]])]
    #determine top left and bottom left points
    if left_points[0][1] > left_points[1][1]:
        top_left = left_points[1]
        bottom_left = left_points[0]
    else:
        top_left = left_points[0]
        bottom_left = left_points[1]
    #determine top right and bottom right points
    if right_points[0][1] > right_points[1][1]:
        top_right = right_points[1]
        bottom_right = right_points[0]
    else:
        top_right = right_points[0]
        bottom_right = right_points[1]
    return (top_left, top_right, bottom_right, bottom_left)

def get_point_mat(p, p_prime):
    x = p[0]
    y = p[1]
    x_p = p_prime[0]
    y_p = p_prime[1]
    p_i = np.array([[-x, -y, -1,  0,  0,  0, x*x_p, y*x_p, x_p],
                    [ 0,  0,  0, -x, -y, -1, x*y_p, y*y_p, y_p]])
    return p_i

def solve_h(p, p_prime):
    A = np.array([])
    for i in range(len(p)):
        p_i = get_point_mat(p[i], p_prime[i])
        if A.size == 0:
            A = p_i
        else:
            A = np.concatenate((A, p_i))
    last = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1])
    A = np.append(A, [last], axis = 0)
    return A

def get_new_xy(x, y, h):
    pretrans = h.dot([x,y,1])
    loc = pretrans/pretrans[2]
    return (round(loc[0]), round(loc[1]))

def main():
    ny_file = sys.argv[1]
    bb_file = sys.argv[2]

    #Source: https://www.kite.com/python/examples/4300/os-remove-the-file-extension-from-a-filename
    output = os.path.splitext(ny_file)[0] + '_output.jpg'
    image = cv2.imread(ny_file, -1)
    bb_img = cv2.imread(bb_file, -1)
    bb_height = bb_img.shape[0]
    bb_width = bb_img.shape[1]

    x_vals = []
    y_vals = []

    param = [image, x_vals, y_vals]
    cv2.namedWindow('Double Click Four Corners. Hit Enter when Done or to Quit')
    cv2.setMouseCallback('Double Click Four Corners. Hit Enter when Done or to Quit', draw_circle, param)

    while True:
        cv2.imshow('Double Click Four Corners. Hit Enter when Done or to Quit', image)
 
        if cv2.waitKey(20) & 0xFF == ord('\x0D'):
            break
    
    if len(x_vals) != 4:
        raise Exception('Please Click Exactly 4 Corners')

    # Corner order:
    # 1 > 2
    # 4 < 3
    ny_corn = make_xy(x_vals, y_vals)
    bb_corn = ((0, 0), (bb_width, 0), (bb_width, bb_height), (0, bb_height))
    #print(ny_corn)
    #print(bb_corn)
    homog = solve_h(bb_corn, ny_corn)
    b = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1])
    x, residuals, rank, s = np.linalg.lstsq(homog,b,rcond=None)
    H = x.reshape((3,3))
    print(H)

    pil_img_ny = Image.open(sys.argv[1]).convert('RGB')
    pil_img_bb = Image.open(sys.argv[2]).convert('RGB')
    
    ny_img_arr = np.array(pil_img_ny)
    bb_img_arr = np.array(pil_img_bb)

    for width in range(bb_width):
        for height in range(bb_height):
            color = bb_img_arr[height][width]
            new_point = get_new_xy(width, height, H)
            pil_img_ny.putpixel(new_point, tuple(color))
            if width == 5 and height == 5:
                print(new_point, color)

    pil_img_ny.show()









if __name__ == '__main__':
    main()














