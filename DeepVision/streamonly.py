#!/usr/bin/env python3

# Routine to stream camera to roborio without any opencv modifications

# import necessary libraries
import argparse
import imutils
import logging
import numpy as np
import wpilib

from cscore import CameraServer
from imutils.video import FPS, VideoStream
from networktables import NetworkTables
from networktables import NetworkTablesInstance

def main():
    # parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", type=int, default=0, help="source id of the camera")
    ap.add_argument("-w", "--width", type=int, default=320, help="set width of the frame")
    ap.add_argument("-l", "--height", type=int, default=240, help="set height of the frame")
    ap.add_argument("-d", "--display", type=int, default=1, help="stream to dashboard")
    ap.add_argument("-n", "--num_frames", type=int, default=500000, help="test frame rate with set number of frames")
    ap.add_argument("-a", "--address", default="10.50.24.2", help="ip address to stream to")
    args = vars(ap.parse_args())

    # setup up logging
    logging.basicConfig(level=logging.DEBUG)

    # connect to the roborio network tables and get the table
    NetworkTables.initialize(server=args["address"])
    sd = NetworkTables.getTable("SmartDashboard")

    # initialize some variables
    width = args["width"]
    height = args["height"]
    numFrames = args["num_frames"]:

    # set up the camera
    vs = VideoStream(src=args["source"]).start()
    fps = FPS().start()

    # setup the stream if required
    if args["display"] > 0:
        camServer = CameraServer.getInstance()
        frameStream = camServer.putVideo("Frame", width, height)

    # initialize frame holders to save time
    frame = np.zeros(shape=(height, width, 3), dtype=np.uint8)

    while fps._numFrames < numFrames
        frame = vs.read()
        frame = imutils.resize(frame, width=width, height=height) 

        if args["display"] > 0:
            frameStream.putFrame(frame)

        # update the fps if set
        if args["num_frames"] > 0:
            fps.update()

    # stop the timer and display the results
    if args["num_frames"] > 0:
        fps.stop()
        print("[INFO] elapsed time: {:.2f} at {:.2f} FPS".format(fps.elapsed(), fps.fps()))

    vs.stop()

if __name__ == "__main__":
    main()

