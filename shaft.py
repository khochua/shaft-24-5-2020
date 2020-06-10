import os
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(
        c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def draw_line_shaft(img_path, save_path):
    img = cv2.imread(img_path)
    tmp_img = img.copy()
    height, width = img.shape[0:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 127, 255)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40,
                            minLineLength=10, maxLineGap=100)
    good = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        print(y2-y1)
        if abs(y2-y1) > 10:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 128), 1)
            good.append(line[0])
    
    if len(good) > 0:
        _xmin, _ymin, _xmax, _ymax = good[0]
        xmin, ymin = line_intersection(
            ((_xmin, _ymin), (_xmax, _ymax)), ((0, 0), (width, 0)))
        xmax, ymax = line_intersection(
            ((_xmin, _ymin), (_xmax, _ymax)), ((0, height), (width, height)))
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
        cv2.line(tmp_img, (xmin, ymin), (xmax, ymax), (128, 0, 128), 2)
        angle = getAngle((xmin, ymin), (xmax, ymax), (0, ymax))
        angle = angle if angle < 180 else 360 - angle
        cv2.putText(tmp_img, str(round(angle, 2)), (int(width/4), int(height-20)),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 127, 255), 1)
        cv2.imwrite(os.path.join(save_path, 'detect_' + os.path.basename(img_path)), tmp_img)
        plt.imshow(tmp_img)
        plt.show()
    return xmin, ymin, xmax, ymax

if __name__ == "__main__":
    image_path = './image'
    save_path = './output'
    for img in os.listdir(image_path):
        if img.endswith(".jpg"):
            im_path = os.path.join(image_path, img)
            draw_line_shaft(im_path, save_path)
