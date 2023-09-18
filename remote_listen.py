#!/usr/bin/python

import RPi.GPIO as GPIO
from lib.janus import janus
import scripts

robot = janus('calibration.ini', test=True)

while(True):
    pass
