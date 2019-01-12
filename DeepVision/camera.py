import cv2

front_cam = None
back_cam = None

def init(ip):
	global front_cam
	global back_cam
	front_cam = cv2.VideoCapture("http://" + ip + ":1182/stream.mjpg")
	# back_cam  = cv2.VideoCapture("http://" + ip + ":1182/stream.mjpg")

def getFront():
	global front_cam
	ret_val, frame = front_cam.read()
	return frame

def getBack():
	global back_cam
	ret_val, frame = back_cam.read()
	return frame