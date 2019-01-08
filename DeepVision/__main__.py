print("Starting DeepVision")

import nt as nt
import camera as camera
import cameracontrol as control
import sys
import requests

if len(sys.argv) == 2:
	roborio_address = sys.argv[1]
else:
	roborio_address = "http://roborio-5024-frc.local:1181"

# Check for frameserver
print("Checking for frameserver...")
try:
	requests.get("http://127.0.0.1/getframe.php")
except:
	print("FATAL! frameserver not found!")
	exit(1)

# check for roborio
try:
	requests.get(roborio_address)
except:
	print("FATAL! Roborio not found or cameraserver disabled!")
	exit(1)

# Init nt
nt.init()

# init vars
last_mode

while True:
	current_mode = nt.getMode()
	
	# Set camera settings
	if current_mode != last_mode:
		if current_mode == nt.robot_mode.sandstorm:
			control.sandstorm()
		elif current_mode == nt.robot_mode.teleop:
			control.teleop()
	
	# skip if in sandstorm (the drivers need to see)
	if current_mode == nt.robot_mode.sandstorm:
		last_mode = current_mode
		continue
	
	# get frame
	
	# parse through grip
	
	# get data
	
	# do stuff
	
	#publish
	
	last_mode = current_mode