print("Starting DeepVision")

import nt as nt
import camera as camera
import cameracontrol as control
import sys
import requests
import grip as grip

if len(sys.argv) == 2:
	roborio_address = sys.argv[1]
else:
	roborio_address = "roborio-5024-frc.local"


# check for roborio
print("Checking for RoboRIO")
try:
	requests.get("http://" +roborio_address+":1181")
	print("Found!")
except:
	print("FATAL! Roborio not found or cameraserver disabled!")
	exit(1)

# Init nt
nt.init(roborio_address)
camera.init(roborio_address)
pipeline = grip.GripPipeline()

# init vars
last_mode = None

while True:
	current_mode = nt.getMode()
	
	# Set camera settings
	if current_mode != last_mode:
		if current_mode == nt.robot_modes.sandstorm:
			control.sandstorm()
		elif current_mode == nt.robot_modes.teleop:
			control.teleop()
	
	# skip if in sandstorm (the drivers need to see)
	if current_mode == nt.robot_modes.sandstorm:
		last_mode = current_mode
		continue
	
	# get frame
	frame = camera.getFront()
	# parse through grip
	pipeline.process(frame)
	contours = pipeline.filter_contours_output
	if (len(contours) == 2):
		rect1 = cv2.minAreaRect(contours[0])
		rect2 = cv2.minAreaRect(contours[1])
		box1  = cv2.boxPoints(rect1)
		box2  = cv2.boxPoints(rect2)
		box1  = cv2.int0(box1)
		box2  = cv2.int0(box2)
		print(box2)
	else:
		continue
	# get data
	
	# do stuff
	
	#publish
	
	last_mode = current_mode