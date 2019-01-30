'''
    FRC 2018-19 Deep Space Challenge
    Automatic Contour Collection and Analysis (ACCA)
'''

print("Starting DeepVision")

# All the good stuffs
import tnt as nt
import camera as camera
import sys
import requests
from cv2 import *
from grip import grip as grip
from scipy.interpolate import interp1d


if len(sys.argv) == 2:
    roborio_address = sys.argv[1]
else:
    roborio_address = "10.50.24.2"
    # [ROBO_RIO ADDRESS HERE ^]

# Boring math ahead --> interpolate one dimension from sci-py
m1  = interp1d([300, 600], [0, 1])
m2 = interp1d([0, 299], [-1, 0])

# Find me that Robo-RIO!!
print("Checking for RoboRIO")

# Init Network Tables
nt.init(roborio_address)
camera.init(roborio_address)

# Initializing GRIP pipeline(boop, beep)
pipeline = grip.GripPipeline()

# Init vars for Calculations in while loop
cameraWidth = 600
fov         = 60
degPerPixel = cameraWidth / fov

while True:

    # Get frame from front camera
    isframe, front_frame = camera.getFront()
    if not isframe:
    	continue
    front_frame = cv2.resize(front_frame, (600, 400))

    # Parse grip profile
    pipeline.process(front_frame)

    # C is for contours and contours are for me
    cookies = pipeline.filter_contours_output

    try:
        x1, _ = cv2.boxPoints(cv2.minAreaRect(cookies[0]))[0]
        x2, _ = cv2.boxPoints(cv2.minAreaRect(cookies[1]))[0]
    except:
        if len(cookies) == 1:
            x1, _ = cv2.boxPoints(cv2.minAreaRect(cookies[0]))[0]
            x2    = x1
        else:
            nt.publish(0.0, 0.0)
            continue

    ''' Math to find the center of 2 contours then use
	their center to calculate the center of those'''
    centre       = (x1 + x2) / 2
    displacement = cameraWidth / 2 - centre
    angle        = displacement / degPerPixel
    # distance     = (max(x1, x2) - min(x1, x2))

    # Print to console {TESTING}
    print(f"{angle} | {len(cookies)}                         ", end="\r")

    # Publish to networks tables.
    nt.publish(angle * -1, angle * -1)