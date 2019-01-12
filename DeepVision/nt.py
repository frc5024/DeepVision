from networktables import NetworkTables
from enum import Enum

robot_modes = Enum("Mode", "sandstorm teleop")

vision_table = None

# Table:
# isTeleop (bool(int))
# nearestX (int)
# nearestY (int)

def init(ip):
	global vision_table
	NetworkTables.initialize(server=ip)
	vision_table = NetworkTables.getTable("SmartDashboard/Vision")

def publish(data):
	global vision_table
	## publish the data
	vision_table.putNumber("Motor", data)

def getMode():
	if bool(vision_table.getNumber("isTeleop", 1.0)):
		return robot_modes.teleop
	else:
		return robot_modes.sandstorm