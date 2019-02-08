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
cameraWidth = 160
fov         = 60
degPerPixel = cameraWidth / fov

while True:

    # Get frame from front camera
    isframe, front_frame = camera.getFront()
    if not isframe:
    	continue

    # Parse grip profile
    pipeline.process(front_frame)

    # C is for contours and contours are for me
    cookies = pipeline.filter_contours_output
    l1 = lambda x: x[0]
    l2 = lambda x: x[1]


    try:
        bx1vert = sorted(cv2.boxPoints(cv2.minAreaRect(cookies[0])),key=l2)
        bx2vert = sorted(cv2.boxPoints(cv2.minAreaRect(cookies[1])),key=l2)
        x1t1, _ = bx1vert[0]
        x1t2, _ = bx1vert[1]

        x2t1, _ = bx2vert[0]
        x2t2, _ = bx2vert[1]

        if(x1t1 > x1t2):
            x1 = x1t1
        else:
            x1 = x1t2
        if(x2t1 > x2t2):
            x2 = x2t1
        else:
            x2 = x2t2

        
    except:
        if len(cookies) == 1:
            bx1sort = sorted(cv2.boxPoints(cv2.minAreaRect(cookies[0])),key=l1)
            x1, _ = bx1sort[1]
            x2    = x1
        else:
            nt.publish(0.0, 0.0)
            continue

    ''' Math to find the center of 2 contours then use
	their center to calculate the center of those'''
    centre       = (x1 + x2) / 2
    displacement = cameraWidth / 2 - centre
    angle        = displacement / degPerPixel
    widthpx     = abs(int(x2 - x1))
    #focal length = width(in px) * distance / width(inches)
    #distance(32) was measured manually
    #8 is distance between 2 closest points, found in game manual
    measuredwidthpx = 35
    widthinch = 8
    measureddistance = 42
    flength = measuredwidthpx * measureddistance / widthinch
    #d' = w(inches) * focal length / w(pixels)
    #so that we don't divide by zero
    if (widthpx > 0):
        #2.54 because we need to convert to cm
        distance = (widthinch * flength / widthpx)
    else:
        distance = 0

    # Print to console {TESTING}
    temp = cv2.boxPoints(cv2.minAreaRect(cookies[0]))
    print(f"1:{distance}| {widthpx}         ", end="\r")
  


    # Publish to networks tables.
    nt.publish(angle * -1, angle * -1)