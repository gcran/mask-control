#!/usr/bin/python

import RPi.GPIO as GPIO
from lib.janus import janus
import scripts

def remote_callback(channel):
    if GPIO.input(channel):
        scripts.welcomeScript(robot)

robot = janus('calibration.ini', test=True)

while(True):
    pass