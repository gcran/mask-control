#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
try:
        id, text = reader.read()
        print(str(id))
        

finally:
        GPIO.cleanup()
