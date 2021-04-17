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

def draw_circle(event, x, y, flags, param):
    height = param[0].shape[0]
    width = param[0].shape[1]
 
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(param[0], (x, y), 5, (255, 0, 0), -1)
 
        # Append values to the list
        param[1].append(x)
        param[2].append(y)

def main():
    ny_file = sys.argv[1]
    bb_file = sys.argv[2]

    #Source: https://www.kite.com/python/examples/4300/os-remove-the-file-extension-from-a-filename
    output = os.path.splitext(ny_file)[0] + '_output.jpg'
    image = cv2.imread(ny_file, -1)

    x_vals = []
    y_vals = []

    param = [image, x_vals, y_vals]
    cv2.namedWindow('Image mouse')
    cv2.setMouseCallback('Image mouse', draw_circle, param)

    while True:
        cv2.imshow('Image mouse', image)
 
        if cv2.waitKey(20) & 0xFF == ord('\x0D'):
            break
    
    if len(x_vals) != 4:
        raise Exception('Please Click Exactly 4 Corners')

    
    print(x_vals)
    print(y_vals)








if __name__ == '__main__':
    main()














