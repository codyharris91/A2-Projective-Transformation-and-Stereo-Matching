import numpy as np
from PIL import Image
import math
import sys


def ssd(a, b):
    return np.sum((a - b) ** 2)

def generate_box(img, x, y, wl, wr, hu, hd):
    w = wl + wr + 1
    h = hu + hd + 1
    start_x = x - wl
    start_y = y - hu
    col_list = []
    for j in range(h):
        row_list = []
        for i in range(w):
            row_list.append(img.getpixel((start_x+i,start_y+j)))
        col_list.append(row_list)
    return np.array(col_list)

def disp_map(img1, img2, window_size=5):
    width, height = img1.size
    s = window_size //2
    disp_arr = np.zeros((height,width))
    for y in range(height):
        for x in range(width):
            wl = min(x, s)
            wr = min(width-1-x, s)
            hu = min(y, s)
            hd = min(height-1-y, s)
            ref_box = generate_box(img1, x, y, wl, wr, hu, hd)
            min_cost = math.inf
            best_d = None
            for x2 in range(wl, width-wr, 1):
                sliding_box = generate_box(img2, x2, y, wl, wr, hu, hd)
                cost = ssd(ref_box, sliding_box)
                if cost < min_cost:
                    min_cost = cost
                    best_d = x2 - x
            disp_arr[y,x] = best_d
    return disp_arr

def end_point_error(pred_img, ground_truth):
    epe = np.mean(abs(pred_img-ground_truth))
    return epe

def error_rate(pred_img, ground_truth, threshold=3):
    disparity = abs(pred_img-ground_truth)>threshold
    er = 100*np.mean(disparity)
    return er

if __name__ == '__main__':
    left_img = sys.argv[1]
    right_img = sys.argv[2]
    ground_truth = sys.argv[3]
    output = sys.argv[4]

    left_img = Image.open(left_img)
    right_img = Image.open(right_img)
    gt_img = Image.open(ground_truth).convert('L')

    w, h = left_img.size

    ratio = w/h
    new_w = int(ratio * 100)
    
    left_img = left_img.resize((new_w,100))
    right_img = right_img.resize((new_w,100))
    gt_img = gt_img.resize((new_w,100))
    gt = np.array(gt_img)

    dp_map = disp_map(left_img, right_img)
    arr_min = dp_map.min(axis = 0).min()
    arr_max = dp_map.max(axis = 0).max()
    dp_st = (((dp_map - arr_min)/(arr_max - arr_min)) * 255).astype(int)
    dp_st = (dp_st - 255) * -1
    dp_st = np.uint8(dp_st)

    im = Image.fromarray(dp_st)
    im.show()
    im.save('output/' + output + '.png')

    epe = end_point_error(dp_st, gt)
    er = error_rate(dp_st, gt)
    print(epe)
    print(er)