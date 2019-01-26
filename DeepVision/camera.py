''' 
    FRC 2018-19 Deep Space Challenge
    Automatic Contour Collection and Analysis (ACCA)
'''

import cv2

front_cam = None
back_cam = None


def init(ip):
    global front_cam
    global back_cam
    # Front camera var
    front_cam = cv2.VideoCapture("http://" + ip + ":1182/stream.mjpg")


# Front camera functions
def getFront():
    global front_cam
    ret_val, frame = front_cam.read()
    return frame


# Back camera functions
def getBack():
    global back_cam
    ret_val, frame = back_cam.read()
    return frame

