#!./.venv/bin/python

from imutils.video import VideoStream
import time
from lib.objcenter import ObjCenter
import argparse
import cv2
import signal
import sys
from multiprocessing import Manager
from multiprocessing import Process

# function to handle keyboard interrupt
def signal_handler(sig, frame):
    # print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")

    # disable the servos
    # pth.servo_enable(1, False)
    # pth.servo_enable(2, False)

    # exit
    sys.exit()

def obj_center(args, objX, objY, centerX, centerY):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # start the video stream and wait for the camera to warm up
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    # initialize the object center finder
    obj = ObjCenter(args["cascade"])

    # loop indefinitely
    while True:
        # grab the frame from the threaded video stream and flip it
        # vertically (since our camera was upside down)
        frame = vs.read()
        frame = cv2.flip(frame, 0)

        # calculate the center of the frame as this is where we will
        # try to keep the object
        (H, W) = frame.shape[:2]
        centerX.value = W // 2
        centerY.value = H // 2

        # find the object's location
        objectLoc = obj.update(frame, (centerX.value, centerY.value))
        ((objX.value, objY.value), rect) = objectLoc

        # extract the bounding box and draw it
        if rect is not None:
            (x, y, w, h) = rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),
                2)
            print(objX.value)
            print(objY.value)

        # display the frame to the screen
        cv2.imshow("Pan-Tilt Face Tracking", frame)
        cv2.waitKey(1)

# check to see if this is the main body of execution
if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", type=str, required=True,
        help="path to input Haar cascade for face detection")
    args = vars(ap.parse_args())

    # start a manager for managing process-safe variables
    with Manager() as manager:
        # enable the servos
        # pth.servo_enable(1, True)
        # pth.servo_enable(2, True)

        # set integer values for the object center (x, y)-coordinates
        centerX = manager.Value("i", 0)
        centerY = manager.Value("i", 0)

        # set integer values for the object's (x, y)-coordinates
        objX = manager.Value("i", 0)
        objY = manager.Value("i", 0)

        # pan and tilt values will be managed by independed PIDs
        pan = manager.Value("i", 0)
        tlt = manager.Value("i", 0)

        processObjectCenter = Process(target=obj_center,
            args=(args, objX, objY, centerX, centerY))
        
        # start all 4 processes
        processObjectCenter.start()
        processObjectCenter.join()