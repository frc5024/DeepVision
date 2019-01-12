print("Starting DeepVision")

import tnt as nt
import camera as camera
import cameracontrol as control
import sys
import requests
import cv2
from grip import grip as grip
from scipy.interpolate import interp1d


if len(sys.argv) == 2:
	roborio_address = sys.argv[1]
else:
	roborio_address = "roborio-5024-frc.local"

#interpolate 1d from scipy
m = interp1d([300, 600], [0,1])
m2 = interp1d([0,299], [-1,0])


# check for roborio
print("Checking for RoboRIO")


#try:
#	requests.get("http://" + roborio_address + ":1181")	
#	print("Found!")
#except:
#	print("FATAL! Roborio not found or cameraserver disabled!")
#
#
#	exit(1)



# Init nt
nt.init(roborio_address)
camera.init(roborio_address)

# init pipeline
pipeline = grip.GripPipeline()


# init vars
last_mode = None
cameraWidth = 600
fov = 60
degPerPixel = cameraWidth / fov



while True:
	current_mode = nt.getMode()
	
	# Set camera settings
	# if current_mode != last_mode:
	# 	if current_mode == nt.robot_modes.sandstorm:
	# 		control.sandstorm()
	# 	elif current_mode == nt.robot_modes.teleop:
	# 		control.teleop()
	
	# # skip if in sandstorm (the drivers need to see)
	# if current_mode == nt.robot_modes.sandstorm:
	# 	last_mode = current_mode
	# 	continue
	
	# get frame
	front_frame = cv2.resize(camera.getFront(), (600,400))
	# back_frame = camera.getBack()
	
	# parse through grip
	pipeline.process(front_frame)
	
	
	# get data
	cnts = pipeline.filter_contours_output
	print(len(cnts))
	try:
		x1,_ = cv2.boxPoints(cv2.minAreaRect(cnts[0]))[0]
		x2,_ = cv2.boxPoints(cv2.minAreaRect(cnts[1]))[0]
	except:
		if len(cnts) == 1 or False:
			x1,_ = cv2.boxPoints(cv2.minAreaRect(cnts[0]))[0]
			x2 = 0
		else:
			nt.publish(0.0,0.0)
			continue
	centre = (x1 + x2)/2
	
	#Distance between camera center and hatch center
	displacement = cameraWidth/2 - centre

	#The angle betwen the center of the robot and hatch center
	angle = displacement/degPerPixel
	
	distance = (max(x1,x2) - min(x1,x2))
	
	
	# do stuff
	# cv2.imshow("Front Cam", front_frame)
	# cv2.imshow("Back Cam", back_frame)
	
	#publish
	nt.publish(angle,angle)
	# print(rotation, end="\r")
	# print(centre)
	
	last_mode = current_mode