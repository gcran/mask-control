#!./.venv/bin/python

from imutils.video import VideoStream
import time
from lib.objcenter import ObjCenter
from lib.pid import pid
from lib.face_motor import face_motor
import argparse
import cv2
import signal
import sys
from multiprocessing import Manager
from multiprocessing import Process
import curses
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import RPi.GPIO as GPIO
import configparser

# function to handle keyboard interrupt
def signal_handler(sig, frame):
    
    pca1.deinit()
    if(test_mode):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    # disable the servos
    # pth.servo_enable(1, False)
    # pth.servo_enable(2, False)
    
    # print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")

    # exit
    sys.exit()

def pid_process(cmd, p, i, d, objCoord, pos, min, max, res):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # create a PID and initialize it
    p = pid(p.value, i.value, d.value)
    p.init_cond()

    # loop indefinitely
    while True:
        # calculate the error
        objAngle = int(((max.value - min.value) / res.value) * objCoord.value + min.value)
        error = pos.value - objAngle

        # update the value
        cmd.value = pos.value + p.update(error)

def obj_center(cascade, objX, objY, centerX, centerY, objFound):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # start the video stream and wait for the camera to warm up
    vs = VideoStream(usePiCamera=True, resolution=(1024, 768),
		framerate=24).start()
    time.sleep(2.0)

    # initialize the object center finder
    obj = ObjCenter(cascade)

    # loop indefinitely
    while True:
        # grab the frame from the threaded video stream and flip it
        # vertically (since our camera was upside down)
        frame = vs.read()
        # frame = cv2.flip(frame, 0)

        # calculate the center of the frame as this is where we will
        # try to keep the object
        (H, W) = frame.shape[:2]
        centerX.value = W // 2
        centerY.value = H // 2

        # find the object's location
        objectLoc = obj.update(frame, (centerX.value, centerY.value))
        ((facex, facey), rect) = objectLoc

        # extract the bounding box and draw it
        if rect is not None:
            objFound.value = True
            (x, y, w, h) = rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),
                2)
            objX.value = facex
            objY.value = facey
        else:
            objFound.value = False
            objX.value = centerX.value
            objY.value = centerY.value
            
        # display the frame to the screen
        cv2.imshow("Pan-Tilt Face Tracking", frame)
        cv2.waitKey(1)

def test_output():
    test_out.addstr(0, 0, '{0:<10}\t{1:>10}\t{2:>10}\t{3:>10}\t{4:>10}'.format(' ', 'objX', 'objY', 'pancmd', 'panpos'))
    test_out.addstr(1, 0, '{0:<10}\t{1:>10}\t{2:>10}\t{3:>10.0f}\t{4:>10.0f}'.format(' ', (((panmax.value - panmin.value) / resX.value) * objX.value + panmin.value), (((tltmax.value - tltmin.value) / resY.value) * objY.value + tltmin.value), pancmd.value, panpos.value))
    test_out.refresh()

def update_servos(pancmd,tltcmd):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # loop indefinitely
    while True:
        # the pancmd and tilt angles are reversed
        panAngle = -1 * pancmd.value
        tiltAngle = -1 * tltcmd.value

        # if the pancmd angle is within the range, pancmd
        panmotor.setCmd(panAngle)
        panmotor.update()

        # if the tilt angle is within the range, tilt
        tiltmotor.setCmd(tiltAngle)
        tiltmotor.update()

        panpos.value = panmotor.getOutput()
        tltpos.value = tiltmotor.getOutput()

        if test_mode:
            test_output()
    
# check to see if this is the main body of execution
if __name__ == "__main__":
    # load calibration file
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cal", type=str, required=True,
        help="path to calibration file")
    args = vars(ap.parse_args())
    calfile = configparser.ConfigParser()
    calfile.read(args['cal'])
    print(args)
    print(calfile['pca.1']['addr'])
    test_mode = True

    # set up test output screen
    statusMsg = ''
    if test_mode:
        test_out = curses.initscr()
        curses.cbreak()
        curses.noecho()
    
    # initialize i2c bus and PCA9685 Modules
    i2c_bus = busio.I2C(SCL, SDA)
    pca1 = PCA9685(i2c_bus, address=int(calfile['pca.1']['addr'], 16))
    pca1.reset()
    pwm1_period = float(calfile['pca.1']['pwm_period'])
    pca1.frequency = round(1/pwm1_period)

    panparams = calfile['eyes.lpan']
    panparams.update(calfile['motor.' + panparams['type']])
    panparams['pwm_period'] = calfile['pca.1']['pwm_period']   
    panmotor = face_motor(pca1, panparams)

    tiltparams = calfile['eyes.ltilt']
    tiltparams.update(calfile['motor.' + tiltparams['type']])
    tiltparams['pwm_period'] = calfile['pca.1']['pwm_period']   
    tiltmotor = face_motor(pca1, tiltparams)

    # start a manager for managing process-safe variables
    with Manager() as manager:
        # enable the servos
        # pth.servo_enable(1, True)
        # pth.servo_enable(2, True)

        # set integer values for the object center (x, y)-coordinates
        centerX = manager.Value("i", 512)
        centerY = manager.Value("i", 384)
        resX = manager.Value("i", 1024)
        resY = manager.Value("i", 768)

        # set integer values for the object's (x, y)-coordinates
        objX = manager.Value("i", 0)
        objY = manager.Value("i", 0)
        objFound = manager.Value("b", False)

        # pancmd and tilt values will be managed by independed PIDs
        pancmd = manager.Value("f", 0)
        tltcmd = manager.Value("f", 0)
        panpos = manager.Value("f", 0)
        tltpos = manager.Value("f", 0)
        panmax = manager.Value("f", float(calfile['eyes.lpan']['llim_angle']))
        panmin = manager.Value("f", float(calfile['eyes.lpan']['ulim_angle']))
        tltmax = manager.Value("f", float(calfile['eyes.ltilt']['llim_angle']))
        tltmin = manager.Value("f", float(calfile['eyes.ltilt']['ulim_angle']))


        # set PID values for panning
        panP = manager.Value("f", float(calfile['eyes.lpan']['kP']))
        panI = manager.Value("f", float(calfile['eyes.lpan']['kI']))
        panD = manager.Value("f", float(calfile['eyes.lpan']['kD']))

        # set PID values for tilting
        tiltP = manager.Value("f", float(calfile['eyes.ltilt']['kP']))
        tiltI = manager.Value("f", float(calfile['eyes.ltilt']['kI']))
        tiltD = manager.Value("f", float(calfile['eyes.ltilt']['kD']))
        
        processObjectCenter = Process(target=obj_center,
            args=(calfile['general']['cascade'], objX, objY, centerX, centerY, objFound))        
        
        processPan = Process(target=pid_process,
            args=(pancmd, panP, panI, panD, objX, panpos, panmin, panmax, resX))        
        
        processTilt = Process(target=pid_process,
            args=(tltcmd, tiltP, tiltI, tiltD, objY, tltpos, panmin, panmax, resX))
        
        processServo = Process(target=update_servos,
                               args=(pancmd,tltcmd))
        
        # start all 4 processes
        processObjectCenter.start()
        processPan.start()
        #processTilt.start()
        processServo.start()
        processObjectCenter.join()
        processPan.join()
        #processTilt.join()
        processServo.join()