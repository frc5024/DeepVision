print("Starting DeepVision")

import nt as nt
import camera as camera
import cameracontrol as control
import sys
import requests

if len(sys.argv) == 2:
	roborio_address = sys.argv[1]
else:
	roborio_address = "roborio-5024-frc.local"


# check for roborio
print("Checking for RoboRIO")
try:
	requests.get(roborio_address)
	print("Found!")
except:
	print("FATAL! Roborio not found or cameraserver disabled!")
	exit(1)

# Init nt
nt.init(roborio_address)

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
	
	# parse through grip
	
	# get data
	
	# do stuff
	
	#publish
	
	last_mode = current_mode