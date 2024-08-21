#!./.venv/bin/python
import cv2
from imutils.video import VideoStream
import time

vs = VideoStream(usePiCamera=True, resolution=(1024, 768),
		framerate=24).start()
time.sleep(2.0)

def repeat():
    global capture #declare as globals since we are assigning to them now
    global camera_index
    frame = vs.read()
    cv2.imshow("Pan-Tilt Face Tracking", frame)
    cv2.waitKey(1)

while True:
    
    repeat()