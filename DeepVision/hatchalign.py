#!/usr/bin/env python3

# import necessary libraries
import argparse
import cv2
import imutils
import json
import logging
import numpy as np
import time
import wpilib

from cscore import CameraServer
from imutils.video import FPS, VideoStream
from networktables import NetworkTables
from networktables import NetworkTablesInstance
from scipy.interpolate import interp1d

def main():
    # parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", type=int, default=0, help="source id of the camera")
    ap.add_argument("-w", "--width", type=int, default=320, help="set width of the frame")
    ap.add_argument("-l", "--height", type=int, default=240, help="set height of the frame")
    ap.add_argument("-d", "--display", type=int, default=1, help="stream to dashboard")
    ap.add_argument("-n", "--num_frames", type=int, default=300000, help="test frame rate with set number of frames")
    ap.add_argument("-a", "--address", default="10.50.24.2", help="ip address to send the streams"
    args = vars(ap.parse_args())

    # setup up logging
    logging.basicConfig(level=logging.DEBUG)

    # connect to the roborio network tables and get the table
    NetworkTables.initialize(server=args["address"])
    sd = NetworkTables.getTable("SmartDashboard")

    # initialize some variables
    numFrames = args["num_frames"]
    width = args["width"]
    height = args["height"]
    min_area = 100
    centerX = width // 2
    distance_between_targets = 11.5
    lX = lY = rX = rY = 0

    # set up the camera
    vs = VideoStream(src=args["source"]).start()
    fps = FPS().start()

    # setup the stream if required
    if args["display"] > 0:
        camServer = CameraServer.getInstance()
        frameStream = camServer.putVideo("Frame", width, height)
        maskStream = camServer.putVideo("Mask", width, height)

    # initialize frame holders to save time
    frame   = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    grayed  = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    blurred = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    hsv     = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    mask    = np.zeros(shape=(height, width, 3), dtype=np.uint8)

    count = 0

    while fps._numFrames < numFrames:
        frame = vs.read()
        frame = imutils.resize(frame, width=width, height=height) # Initially 370 FPS

        # gray, blur frame and convert it to hsv color space
        # grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # drops FPS to 1.5 with blur
        # blurred = cv2.GaussianBlur(frame, (3, 3), 0)  # drops FPS to 2
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # drops FPS to 1.5 with blur

        # get the bounds from the dashboard
        lH = sd.getNumber("H-Lower", 0)
        uH = sd.getNumber("H-Upper", 180)

        lS = sd.getNumber("S-Lower", 0)
        uS = sd.getNumber("S-Upper", 255)

        lV = sd.getNumber("V-Lower", 0)
        uV = sd.getNumber("V-Upper", 255)

        # construct a mask for the bounds then erode and dilate it
        mask = cv2.inRange(hsv, (lH, lS, lV), (uH, uS, uV))  # drops FPS to 10 wihout blur
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # find closest contours to center on each side
        min_left = 0
        min_right = width
        left_contour = None
        right_contour = None

        # loop through contours
        for c in cnts:
            area = cv2.contourArea(c)

            # look only at contours larger than the min_area
            if area > min_area:
                M = cv2.moments(c)
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))

                ((x, y), radius) = cv2.minEnclosingCircle(c)

                # draw a blue circle around the contour
                cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 0), 1)

                # find the contours closest to the center x-value of the frame
                if cX > centerX:
                    if cX < min_right:
                        min_right = cX
                        right_contour = c
                else:
                    if cX > min_left:
                        min_left = cX
                        left_contour = c

        # draw a yellow circle around the nearest contours
        if right_contour is not None:
            ((rX, rY), radius) = cv2.minEnclosingCircle(right_contour)
            cv2.circle(frame, (int(rX), int(rY)), int(radius), (0, 255, 255), 1)

        if left_contour is not None:
            ((lX, lY), radius) = cv2.minEnclosingCircle(left_contour)
            cv2.circle(frame, (int(lX), int(lY)), int(radius), (0, 255, 255), 1)

        # interplate the distance between the centers of the two nearest contours for 11.5 inches
        if lX > 0 and rX > 0:
            try:
                distance = interp1d([lX, rX], [0, distance_between_targets])
                distance_from_left = distance(centerX)
                offset_from_center = (distance_between_targets / 2) - distance_from_left
                sd.putNumber("Offset", offset_from_center)
            except (NameError, ValueError) as e:
                # print("Error in interpolation", e)
                pass

        # draw a center line
        # cv2.line(frame, (centerX, 0), (centerX, height), (255, 255, 255), 1)

        if args["display"] > 0:
            frameStream.putFrame(frame)
            maskStream.putFrame(mask)

        # update the fps if set
        if numFrames > 0:
            fps.update()

    # stop the timer and display the results
    if numFrames > 0:
        fps.stop()
        print("[INFO] elapsed time: {:.2f} at approx {:.2f} FPS".format(fps.elapsed()), format(fps.fps()))

    vs.stop()

if __name__ == "__main__":
    main()

